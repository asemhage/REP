class UserProfile {
  const UserProfile({
    required this.id,
    required this.username,
    required this.role,
    this.firstName,
    this.lastName,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'] as int,
      username: json['username'] as String? ?? '',
      role: json['role'] as String? ?? '',
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
    );
  }

  final int id;
  final String username;
  final String role;
  final String? firstName;
  final String? lastName;
}
