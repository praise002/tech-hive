import PropTypes from 'prop-types';

function Tags({ tags }) {
  return (
    <div className="flex gap-2 flex-wrap my-2 text-xs md:text-sm">
      {tags.map((tag, index) => (
        <div key={index} className="inline-flex items-center">
          <span className={tag.color}>#</span>
          <span className="dark:text-custom-white">{tag.name}</span>
        </div>
      ))}
    </div>
  );
}

Tags.propTypes = {
  tags: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      color: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default Tags;
