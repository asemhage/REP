import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/login_request.dart';
import '../state/auth_notifier.dart';

class LoginForm extends StatefulWidget {
  const LoginForm({super.key});

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    final auth = context.read<AuthNotifier>();
    final success = await auth.login(
      LoginRequest(
        username: _usernameController.text.trim(),
        password: _passwordController.text,
      ),
    );
    if (!mounted) return;

    if (success) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('تم تسجيل الدخول بنجاح')),
        );
      }
    } else {
      final error = auth.error ?? 'حدث خطأ أثناء التسجيل';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error)));
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthNotifier>();

    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextFormField(
            controller: _usernameController,
            decoration: const InputDecoration(labelText: 'اسم المستخدم'),
            validator: (value) => (value == null || value.isEmpty) ? 'أدخل اسم المستخدم' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'كلمة المرور'),
            obscureText: true,
            validator: (value) => (value == null || value.isEmpty) ? 'أدخل كلمة المرور' : null,
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: auth.isLoading ? null : _submit,
            child: auth.isLoading
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('تسجيل الدخول'),
          ),
        ],
      ),
    );
  }
}
