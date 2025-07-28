import { Link } from 'react-router-dom';
import { FaSquareFacebook, FaXTwitter } from 'react-icons/fa6';
import { FaInstagram, FaLinkedin } from 'react-icons/fa';
import { SocialIcon } from '../common/SocialIcon';

// use max-width or w-full
function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = [
    { to: '/', name: 'Home' },
    { to: '/categories', name: 'Categories' },
    { to: '/about', name: 'About Us' },
    { to: '/contact', name: 'Contact Us' },
  ];

  const otherLinks = [
    { href: '#legal', name: 'Legal' },
    { href: '#privacy', name: 'Privacy Policy' },
    { href: '#termsofservice', name: 'Terms of Service' },
  ];

  const socialIcon = {
    x: 'http://',
    fb: 'http://',
    ln: 'http://',
    ig: 'http://',
  };

  return (
    <footer className="text-gray-100 bg-red-800">
      <div className="max-w-7xl mx-auto py-12 px-4 lg:px-8">
        <div className="grid md:grid-cols-4 gap-6 text-center md:text-left">
          <div className="uppercase  text-xl font-bold">
            <span className="text-orange-dark">Tec</span>Hive.
          </div>
          <nav aria-label="Footer main navigation">
            <ul className="flex flex-col space-y-4 text-sm">
              {footerLinks.map((link) => (
                <li key={link.to}>
                  <Link
                    to={link.to}
                    className="hover:text-gray-300 transition-colors"
                    aria-label={`Go to ${link.name}`}
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          <nav aria-label="Footer legal navigation">
            <ul className="flex flex-col space-y-4 text-sm">
              {otherLinks.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className="hover:text-gray-300 transition-colors"
                    aria-label={`Read ${link.name}`}
                  >
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <ul
            className="flex justify-center md:items-start space-x-4 mt-4 md:mt-0"
            aria-label="Social media links"
          >
            {socialIcon.x && (
              <SocialIcon
                ariaLabel="Follow us on X (Twitter)"
                href="http://"
                icon={FaXTwitter}
              />
            )}
            {socialIcon.fb && (
              <SocialIcon
                ariaLabel="Follow us on Facebook"
                href="http://"
                icon={FaSquareFacebook}
              />
            )}
            {socialIcon.ln && (
              <SocialIcon
                ariaLabel="Follow us on LinkedIn"
                href="http://"
                icon={FaLinkedin}
              />
            )}
            {socialIcon.ig && (
              <SocialIcon
                ariaLabel="Follow us on Instagram"
                href="http://"
                icon={FaInstagram}
              />
            )}
          </ul>
        </div>
        <div
          className="mt-10 text-center text-xs"
          aria-label="Copyright notice"
        >
          © {currentYear} Tech Hive. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
}

export default Footer;
