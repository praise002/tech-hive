import { useState } from 'react';
import { CiSearch } from 'react-icons/ci';
import { IoFilterOutline } from 'react-icons/io5';
import TableCell from './TableCell';
import StatusSpan from './StatusSpan';
import RoleSpan from './RoleSpan';

function ManageContent() {
  const [activeRowIndex, setActiveRowIndex] = useState<number | null>(null);

  const contentStats = [
    { label: 'All posts', count: 24 },
    { label: 'Drafts', count: 2 },
    { label: 'Submitted', count: 7 },
    { label: 'Published', count: 18 },
    { label: 'Rejected', count: 2 },
  ];

  const tableHeaders = [
    { key: 'title', label: 'Post Title' },
    { key: 'author', label: 'Author' },
    { key: 'date', label: 'Date' },
    { key: 'role', label: 'Role' },
    { key: 'status', label: 'Status' },
    { key: 'action', label: 'Action' },
  ];

  const tableData = [
    {
      title: 'The Future of UI/UX: Trends...',
      author: 'TECHIVE',
      date: '29/12/24',
      role: 'Admin',
      status: 'Published',
    },
    {
      title: 'The rise of blockchain in Re...',
      author: 'Adeyinka Favor',
      date: '26/12/24',
      role: 'Contributor',
      status: 'Published',
    },
    {
      title: 'AI-Powered Marketing Strategies',
      author: 'Jane Doe',
      date: '20/12/24',
      role: 'Editor',
      status: 'Rejected',
    },
    {
      title: 'Cybersecurity Best Practices',
      author: 'Robert Smith',
      date: '15/12/24',
      role: 'Reviewer',
      status: 'Rejected',
    },
    {
      title: 'Cloud Computing Trends',
      author: 'Alice Johnson',
      date: '10/12/24',
      role: 'Admin',
      status: 'Published',
    },
    {
      title: 'The Impact of IoT on Industries',
      author: 'David Lee',
      date: '05/12/24',
      role: 'Contributor',
      status: 'Published',
    },
    {
      title: 'Data Science for Beginners',
      author: 'Emily White',
      date: '01/12/24',
      role: 'Editor',
      status: 'Rejected',
    },
    {
      title: 'Mobile App Development Tips',
      author: 'Michael Brown',
      date: '25/11/24',
      role: 'Reviewer',
      status: 'Rejected',
    },
    {
      title: 'The Future of Work',
      author: 'Sarah Green',
      date: '20/11/24',
      role: 'Admin',
      status: 'Published',
    },
    {
      title: 'Ethical Considerations in AI',
      author: 'Kevin Black',
      date: '15/11/24',
      role: 'Contributor',
      status: 'Published',
    },
  ];

  return (
    <>
      <div>
        <div className="my-6 lg:my-0 mx-6 flex flex-col lg:flex-row gap-4 justify-between text-primary dark:text-custom-white">
          {contentStats.map(({ label, count }) => (
            <div
              key={label}
              className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200"
            >
              <span className="font-medium">{label}</span>
              <span className="font-semibold">{count}</span>
            </div>
          ))}
        </div>
        <div>
          <div className="relative hidden lg:flex lg:justify-end my-6 mr-6">
            <div className="relative">
              {/* Search Icon */}
              <CiSearch className="text-xl absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />

              {/* Input Field */}
              <input
                className="appearance-none w-70 dark:text-custom-white border border-gray-500 dark:border-custom-white rounded-md pl-10 pr-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-600 dark:focus-visible:ring-white dark:focus-visible:text-white focus-visible:border-gray-600 dark:focus-visible:border-white"
                type="search"
                placeholder="Find posts by title..."
              />
              <IoFilterOutline className="text-xl absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 dark:text-custom-white" />
            </div>
          </div>
        </div>
        <div>
          <table className="min-w-full text-left rtl:text-right">
            <caption className="sr-only">
              A summary of the content&apos;s table
            </caption>
            <thead className="hidden lg:table-header-group">
              <tr className="font-bold">
                {tableHeaders.map(({ key, label }) => (
                  <th key={key} scope="col" className="px-6 py-3">
                    {label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="lg:text-base lg:divide-y-0 text-sm divide-y divide-gray-200 dark:divide-gray-700">
              {tableData.map(({ title, author, date, role, status }, index) => (
                <tr key={title} className="space-y-2 lg:space-y-0">
                  <TableCell className="lg:py-4 pt-2 lg:pt-0">
                    {title}
                  </TableCell>

                  <TableCell className="lg:py-4">{author}</TableCell>

                  <TableCell className="lg:py-4">{date}</TableCell>
                  <TableCell className="py-4 lg:py-0">
                    <RoleSpan role={role} />
                  </TableCell>
                  <TableCell className="py-2 lg:py-0">
                    <StatusSpan status={status} />
                  </TableCell>
                  <td className="px-6 py-4 cursor-pointer relative">
                    <button
                      type="button"
                      onClick={() =>
                        setActiveRowIndex(
                          activeRowIndex === index ? null : index
                        )
                      }
                    >
                      ...
                    </button>
                    {activeRowIndex === index && (
                      <div className="absolute top-15 right-12">
                        <div className="relative bg-custom-white text-gray-800 gap-2 py-3 px-5 w-50 flex flex-col items-start rounded-md">
                          {/* TODO: UNSURE FOR NOW */}
                          <button>View Details</button>
                          <button>Publish/Reject</button>
                          <button>Provide Feedback</button>

                          <div
                            className="absolute -top-3 right-3 w-4 h-4 bg-white"
                            style={{
                              clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)',
                            }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default ManageContent;
