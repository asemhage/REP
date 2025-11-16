import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';

import 'src/app_theme.dart';
import 'src/app_router.dart';
import 'src/features/auth/state/auth_notifier.dart';
import 'src/features/home/state/property_notifier.dart';
import 'src/core/storage/token_storage.dart';
import 'src/core/network/api_client.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  final tokenStorage = TokenStorage();
  final apiClient = ApiClient(tokenStorage: tokenStorage);

  runApp(RealEstateApp(
    tokenStorage: tokenStorage,
    apiClient: apiClient,
  ));
}

class RealEstateApp extends StatelessWidget {
  const RealEstateApp({
    super.key,
    required this.tokenStorage,
    required this.apiClient,
  });

  final TokenStorage tokenStorage;
  final ApiClient apiClient;

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
            create: (_) =>
                AuthNotifier(apiClient: apiClient, tokenStorage: tokenStorage)),
        ChangeNotifierProvider(
            create: (_) => PropertyNotifier(apiClient: apiClient)),
      ],
      child: MaterialApp.router(
        title: 'منصة الحجوزات الليبية',
        routerConfig: AppRouter.router,
        theme: AppTheme.light,
        debugShowCheckedModeBanner: false,
        locale: const Locale('ar'),
        supportedLocales: const [Locale('ar'), Locale('en')],
        localizationsDelegates: const [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
      ),
    );
  }
}
