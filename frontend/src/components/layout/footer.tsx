export const Footer = () => (
  <footer className="border-t border-gray-200 bg-white">
    <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-6 text-sm text-gray-600 md:flex-row md:items-center md:justify-between">
      <span>© {new Date().getFullYear()} منصة الحجوزات الليبية. جميع الحقوق محفوظة.</span>
      <div className="flex gap-6">
        <a href="/privacy" className="hover:text-blue-600">
          سياسة الخصوصية
        </a>
        <a href="/terms" className="hover:text-blue-600">
          الشروط والأحكام
        </a>
        <a href="mailto:support@example.com" className="hover:text-blue-600">
          تواصل معنا
        </a>
      </div>
    </div>
  </footer>
);

