import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/property_notifier.dart';
import '../models/property_summary.dart';

class PropertyList extends StatelessWidget {
  const PropertyList({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<PropertyNotifier>(
      builder: (context, notifier, _) {
        if (notifier.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        if (notifier.errorMessage != null) {
          return Center(child: Text(notifier.errorMessage!));
        }
        if (notifier.featuredProperties.isEmpty) {
          return const Center(child: Text('لا توجد عقارات متاحة حالياً.'));
        }
        return ListView.separated(
          itemCount: notifier.featuredProperties.length,
          separatorBuilder: (_, __) => const SizedBox(height: 12),
          itemBuilder: (context, index) {
            final property = notifier.featuredProperties[index];
            return _PropertyCard(property: property);
          },
        );
      },
    );
  }
}

class _PropertyCard extends StatelessWidget {
  const _PropertyCard({required this.property});

  final PropertySummary property;

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(property.title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('${property.city} • ${property.propertyType}'),
            const SizedBox(height: 8),
            if (property.dailyRate != null)
              Text('السعر اليومي: ${property.dailyRate} دينار', style: const TextStyle(color: Colors.blueAccent)),
            const SizedBox(height: 8),
            Text('الحالة: ${property.status}', style: const TextStyle(color: Colors.green)),
          ],
        ),
      ),
    );
  }
}
