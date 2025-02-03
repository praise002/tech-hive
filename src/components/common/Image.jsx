import PropTypes from 'prop-types';

function Image({ src, alt }) {
  return (
    <div>
      <img src={src} alt={alt} className="max-w-full h-full object-cover" />
       {/* h-full */}
    </div>
  );
}

export default Image;

Image.propTypes = {
  src: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
};

// transition-transform duration-300 hover:scale-105 hover:-translate-y-4
// change to image and reuse everywhere, use props
