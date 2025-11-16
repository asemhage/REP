import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../../home/state/property_notifier.dart';
import '../state/auth_notifier.dart';
import '../widgets/login_form.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _attemptRestore());
  }

  Future<void> _attemptRestore() async {
    final auth = context.read<AuthNotifier>();
    final restored = await auth.tryRestoreSession();
    if (!mounted) return;
    if (restored) {
      context.read<PropertyNotifier>().loadFeatured();
      context.go('/');
    }
  }

  void _onLoginSuccess() {
    context.read<PropertyNotifier>().loadFeatured();
    context.go('/');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 400),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'مرحباً بعودتك',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'سجّل دخولك لمتابعة إدارة حجوزاتك والعربون بسهولة.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 24),
                  LoginForm(key: UniqueKey()),
                  const SizedBox(height: 12),
                  Consumer<AuthNotifier>(
                    builder: (context, auth, _) {
                      if (auth.isAuthenticated) {
                        WidgetsBinding.instance.addPostFrameCallback((_) => _onLoginSuccess());
                      }
                      return const SizedBox.shrink();
                    },
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
