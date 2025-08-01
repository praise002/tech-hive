interface TableCellProps {
  children: React.ReactNode;
  className: string;
}

function TableCell({ children, className }: TableCellProps) {
  return (
    <td className={`px-6 whitespace-nowrap lg:table-cell block ${className}`}>
      {children}
    </td>
  );
}

export default TableCell;
