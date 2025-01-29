import { Link } from 'react-router-dom';
import { FaSquareFacebook, FaXTwitter } from 'react-icons/fa6';
import { FaInstagram, FaLinkedin } from 'react-icons/fa';
import { SocialIcon } from '../common/SocialIcon';

function Footer() {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="text-gray-100 bg-red-800">
      <div className="container mx-auto py-12 px-4">
        <div className="grid md:grid-cols-4 gap-6 text-center md:text-left">
          <div className="uppercase  text-xl font-bold">
            <span className="text-[#d67917]">Tec</span>Hive.
          </div>
          <ul className="flex flex-col space-y-4 text-sm">
            <li>
              <Link to="/" className="hover:text-gray-300 transition-colors">
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/categories"
                className="hover:text-gray-300 transition-colors"
              >
                Categories
              </Link>
            </li>
            <li>
              <Link
                to="/about"
                className="hover:text-gray-300 transition-colors"
              >
                About Us
              </Link>
            </li>
            <li>
              <Link
                to="/contact"
                className="hover:text-gray-300 transition-colors"
              >
                Contact Us
              </Link>
            </li>
          </ul>
          <ul className="flex flex-col space-y-4 text-sm">
            <li>
              <a
                href="#legal"
                className="hover:text-gray-300 transition-colors"
              >
                Legal
              </a>
            </li>
            <li>
              <a
                href="#privacy"
                className="hover:text-gray-300 transition-colors"
              >
                Privacy Policy
              </a>
            </li>
            <li>
              <a
                href="#terms"
                className="hover:text-gray-300 transition-colors"
              >
                Terms of Service
              </a>
            </li>
          </ul>

          <ul className="flex justify-center md:items-start space-x-4 mt-4 md:mt-0">
            <SocialIcon href="http://" icon={FaXTwitter} />
            <SocialIcon href="http://" icon={FaSquareFacebook} />
            <SocialIcon href="http://" icon={FaLinkedin} />
            <SocialIcon href="http://" icon={FaInstagram} />
          </ul>
        </div>
        <div className="mt-10 text-center text-xs">
          © {currentYear} Tech Hive. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
}

export default Footer;
