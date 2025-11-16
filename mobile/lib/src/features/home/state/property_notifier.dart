import 'dart:convert';

import 'package:flutter/foundation.dart';

import '../../../core/constants/endpoints.dart';
import '../../../core/network/api_client.dart';
import '../models/property_summary.dart';

class PropertyNotifier extends ChangeNotifier {
  PropertyNotifier({required this.apiClient});

  final ApiClient apiClient;

  bool _loading = false;
  List<PropertySummary> _featured = const [];
  String? _error;

  bool get isLoading => _loading;
  List<PropertySummary> get featuredProperties => _featured;
  String? get errorMessage => _error;

  Future<void> loadFeatured() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await apiClient.get(ApiConfig.featuredProperties);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List<dynamic>;
        _featured = data
            .map((item) => PropertySummary.fromJson(item as Map<String, dynamic>))
            .toList(growable: false);
      } else {
        _error = 'فشل في تحميل العقارات. رمز ${response.statusCode}';
      }
    } catch (error) {
      _error = 'حدث خطأ في الاتصال: $error';
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  void reset() {
    _featured = const [];
    notifyListeners();
  }
}
