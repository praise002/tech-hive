import PropTypes from 'prop-types';

function Image({ src, alt, className, imgClassName }) {
  return (
    <div className={className}>
      <img
        src={src}
        alt={alt}
        className={`w-full h-full object-cover ${imgClassName}`}
      />
      {/* h-full */}
    </div>
  );
}

export default Image;

Image.propTypes = {
  src: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  className: PropTypes.string,
  imgClassName: PropTypes.string,
};

// transition-transform duration-300 hover:scale-105 hover:-translate-y-4
// change to image and reuse everywhere, use props
