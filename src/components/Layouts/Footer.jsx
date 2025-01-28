import Logo from './Logo';
import { CiPhone, CiYoutube } from 'react-icons/ci';
import { HiOutlineMail } from 'react-icons/hi';
import { IoLocationOutline } from 'react-icons/io5';
import { FaXTwitter } from 'react-icons/fa6';
import { FaFacebookF, FaInstagram, FaWhatsapp } from 'react-icons/fa';
import { SocialIcon } from './SocialIcon';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full">
      <div className="bg-customGray text-white py-12">
        <div className="px-3 md:px-6 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col">
            <Logo className="mb-4" />
            <p>Jonathan Avwunudiogba Family Foundation.</p>
            <p>Together, we can make this world a better place.</p>
          </div>

          <div className="flex flex-col">
            <h5 className="font-bold mb-4 text-lime-500 text-2xl md:text-3xl">
              Contact Information
            </h5>
            <div className="space-y-2">
              <p className="flex items-center space-x-2">
                <CiPhone className="text-white" />
                <a
                  href="tel:+6512785633"
                  className="hover:text-lime-500 transition-colors"
                >
                  +6512785633
                </a>
              </p>
              <p className="flex items-center space-x-2">
                <HiOutlineMail className="text-white" />
                <a
                  href="mailto:donate@foundation.org"
                  className="hover:text-lime-500 transition-colors"
                >
                  donate@foundation.org
                </a>
              </p>
              <p className="flex items-center space-x-2">
                <IoLocationOutline className="text-white" />
                <span>6019 Idsen Lane South Cottage Groove Mn 5</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-purple-700 text-white py-6">
        <div className="px-3 md:px-6 flex flex-col sm:flex-row justify-between items-center">
          <div>Copyright © {currentYear} JAFF Org.</div>
          <ul className="flex space-x-2 mt-4 md:mt-0">
            <SocialIcon href="http://" icon={FaXTwitter} />
            <SocialIcon href="http://" icon={FaFacebookF} />
            <SocialIcon href="http://" icon={FaInstagram} />
            <SocialIcon href="http://" icon={FaWhatsapp} />
            <SocialIcon href="http://" icon={CiYoutube} />
          </ul>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
