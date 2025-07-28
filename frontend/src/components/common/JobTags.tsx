import { JobTagsProps } from '../../types/types';

function JobTags({ tags }: JobTagsProps) {
  return (
    <ul className="flex gap-2 flex-wrap mb-4">
      {tags.map((tag) => (
        <li key={tag}>
          <span className="inline-flex items-center px-2 py-1 bg-cream text-xs font-medium text-gray-700 rounded-sm">
            {tag}
          </span>
        </li>
      ))}
    </ul>
  );
}

export default JobTags;
