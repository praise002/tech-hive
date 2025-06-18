import PropTypes from 'prop-types';

function JobTags({ tags }) {
  return (
    <div className="flex gap-2 flex-wrap mb-4">
      {tags.map((tag, index) => (
        <span
          key={index}
          className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-sm"
        >
          {tag}
        </span>
      ))}
    </div>
  );
}

JobTags.propTypes = {
  tags: PropTypes.array.isRequired,
};

export default JobTags;
