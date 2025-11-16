import 'dart:convert';

import 'package:flutter/foundation.dart';

import '../../../core/constants/endpoints.dart';
import '../../../core/network/api_client.dart';
import '../../../core/storage/token_storage.dart';
import '../models/login_request.dart';
import '../models/login_response.dart';
import '../models/user_profile.dart';

class AuthNotifier extends ChangeNotifier {
  AuthNotifier({required this.apiClient, required this.tokenStorage});

  final ApiClient apiClient;
  final TokenStorage tokenStorage;

  bool _loading = false;
  UserProfile? _currentUser;
  String? _error;

  bool get isLoading => _loading;
  UserProfile? get currentUser => _currentUser;
  String? get error => _error;
  bool get isAuthenticated => _currentUser != null;

  Future<bool> tryRestoreSession() async {
    final token = await tokenStorage.readToken();
    if (token == null || token.isEmpty) {
      return false;
    }
    return await fetchProfile();
  }

  Future<bool> login(LoginRequest request) async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await apiClient.post(
        ApiConfig.login,
        body: ApiClient.encodeBody(request.toJson()),
      );
      if (response.statusCode == 200) {
        final payload = jsonDecode(response.body) as Map<String, dynamic>;
        final loginResponse = LoginResponse.fromJson(payload);
        await tokenStorage.saveToken(loginResponse.token);
        return await fetchProfile();
      } else {
        _error = 'بيانات تسجيل الدخول غير صحيحة';
      }
    } catch (e) {
      _error = 'تعذّر الاتصال بالخادم: $e';
    } finally {
      _loading = false;
      notifyListeners();
    }
    return false;
  }

  Future<bool> fetchProfile() async {
    try {
      final response = await apiClient.get(ApiConfig.me);
      if (response.statusCode == 200) {
        final json = jsonDecode(response.body) as Map<String, dynamic>;
        _currentUser = UserProfile.fromJson(json);
        notifyListeners();
        return true;
      } else {
        _error = 'فشل تحميل الملف الشخصي';
        notifyListeners();
      }
    } catch (e) {
      _error = 'خطأ أثناء تحميل الملف الشخصي: $e';
      notifyListeners();
    }
    return false;
  }

  Future<void> logout() async {
    await tokenStorage.clearToken();
    _currentUser = null;
    notifyListeners();
  }
}
