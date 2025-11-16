class PropertySummary {
  const PropertySummary({
    required this.id,
    required this.title,
    required this.city,
    required this.propertyType,
    required this.status,
    this.dailyRate,
    this.media,
  });

  factory PropertySummary.fromJson(Map<String, dynamic> json) {
    final mediaList = (json['media'] as List?)?.cast<Map<String, dynamic>>();
    return PropertySummary(
      id: json['id'] as int,
      title: json['title'] as String? ?? '',
      city: json['city'] as String? ?? '',
      propertyType: json['property_type'] as String? ?? '',
      status: json['status'] as String? ?? '',
      dailyRate: json['daily_rate']?.toString(),
      media: mediaList
          ?.map(
            (item) => PropertyMedia(
              id: item['id'] as int,
              file: item['file'] as String? ?? '',
              isPrimary: item['is_primary'] as bool? ?? false,
            ),
          )
          .toList(),
    );
  }

  final int id;
  final String title;
  final String city;
  final String propertyType;
  final String status;
  final String? dailyRate;
  final List<PropertyMedia>? media;
}

class PropertyMedia {
  const PropertyMedia({required this.id, required this.file, required this.isPrimary});

  final int id;
  final String file;
  final bool isPrimary;
}
