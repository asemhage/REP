import 'dart:convert';
import 'package:http/http.dart' as http;

import '../constants/endpoints.dart';
import '../storage/token_storage.dart';

class ApiClient {
  ApiClient({required this.tokenStorage});

  final TokenStorage tokenStorage;

  Future<http.Response> post(
    String path, {
    Map<String, String>? headers,
    Object? body,
  }) async {
    final uri = Uri.parse('${ApiConfig.baseUrl}$path');
    final requestHeaders = await _buildHeaders(headers);
    return http.post(uri, headers: requestHeaders, body: body);
  }

  Future<http.Response> get(
    String path, {
    Map<String, String>? headers,
    Map<String, dynamic>? query,
  }) async {
    final uri = Uri.parse('${ApiConfig.baseUrl}$path').replace(queryParameters: query);
    final requestHeaders = await _buildHeaders(headers);
    return http.get(uri, headers: requestHeaders);
  }

  Future<Map<String, String>> _buildHeaders(Map<String, String>? headers) async {
    final token = await tokenStorage.readToken();
    final baseHeaders = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (token != null && token.isNotEmpty) {
      baseHeaders['Authorization'] = 'Token $token';
    }
    if (headers != null) {
      baseHeaders.addAll(headers);
    }
    return baseHeaders;
  }

  static String encodeBody(Map<String, dynamic> data) => jsonEncode(data);
}
