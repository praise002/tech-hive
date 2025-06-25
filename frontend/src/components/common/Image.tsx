import { ImageProps } from '../../types/types';

function Image({ src, alt, className, imgClassName }: ImageProps) {
  return (
    <div className={className}>
      <img
        src={src}
        alt={alt}
        className={`w-full h-full object-cover ${imgClassName}`}
      />
    </div>
  );
}

export default Image;

// transition-transform duration-300 hover:scale-105 hover:-translate-y-4
// change to image and reuse everywhere, use props
