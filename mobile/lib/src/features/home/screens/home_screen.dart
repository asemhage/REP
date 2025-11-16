import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../../auth/state/auth_notifier.dart';
import '../state/property_notifier.dart';
import '../widgets/property_list.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PropertyNotifier>().loadFeatured();
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthNotifier>();

    return Scaffold(
      appBar: AppBar(
        title: Text('مرحباً ${auth.currentUser?.firstName ?? auth.currentUser?.username ?? ''}'),
        actions: [
          TextButton(
            onPressed: () async {
              await context.read<AuthNotifier>().logout();
              context.read<PropertyNotifier>().reset();
              if (context.mounted) {
                context.go('/login');
              }
            },
            child: const Text('تسجيل الخروج'),
          ),
        ],
      ),
      body: const Padding(
        padding: EdgeInsets.all(16),
        child: PropertyList(),
      ),
    );
  }
}
