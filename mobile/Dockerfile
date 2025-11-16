FROM flutterapp/flutter:3.16 AS base

WORKDIR /app

COPY pubspec.yaml pubspec.lock* ./

RUN flutter pub get

COPY . .

CMD ["flutter", "run"]

