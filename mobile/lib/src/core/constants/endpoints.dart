class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000/api/v1',
  );

  static const String login = '/accounts/auth/login/';
  static const String me = '/accounts/users/me/';
  static const String featuredProperties = '/listings/properties';
}
