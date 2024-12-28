import 'package:flutter/material.dart';
import '../../../core/api_service.dart';
import 'package:museic/presentation/pages/songEntity.dart'; // Gerekli entity'ler için import
import 'package:museic/alternative/helper/router.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:http/http.dart' as http;
import 'package:sizer/sizer.dart';
import 'dart:convert';



class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final ApiService _apiService = ApiService(); // ApiService nesnesi

  // Giriş yapma fonksiyonu
  Future<void> _login() async {
    String username = _usernameController.text;
    String password = _passwordController.text;

    if (username.isEmpty || password.isEmpty) {
      _showError('Lütfen tüm alanları doldurun.');
      return;
    }

    try {
      // ApiService kullanarak login işlemi
      final response = await _apiService.loginUser(username, password);
      
      // Başarılı giriş
      if (response != null) {
        // Başarılı giriş sonrası ana sayfaya yönlendirme yapılabilir
        Navigator.pushReplacementNamed(context, '/home');
      }
    } catch (e) {
      // Hata durumunda kullanıcıya mesaj göster
      _showError('Giriş başarısız. Lütfen tekrar deneyin.');
    }
  }

  // Hata mesajı gösterme fonksiyonu
  void _showError(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Hata'),
          content: Text(message),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text('Tamam'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Giriş Yap'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _usernameController, // email yerine username kullanıyoruz
              decoration: InputDecoration(labelText: 'Kullanıcı Adı'),
            ),
            SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: InputDecoration(labelText: 'Şifre'),
              obscureText: true,
            ),
            SizedBox(height: 32),
            ElevatedButton(
              onPressed: _login,
              child: Text('Giriş Yap'),
            ),
          ],
        ),
      ),
    );
  }
}
