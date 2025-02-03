function Tags() {
  return (
    <div className="flex gap-2 flex-wrap my-2">
      {/* Tag 1 */}
      <div className="inline-flex items-center text-sm">
        <span className="text-[#960299]">#</span>
        <span>UIUXDesign</span>
      </div>

      {/* Tag 2 */}
      <div className="inline-flex items-center text-sm">
        <span className="text-[#F58F29]">#</span>
        <span>UserExperience</span>
      </div>

      {/* Tag 3 */}
      <div className="inline-flex items-center text-sm">
        <span className="text-[#DF24A7]">#</span>
        <span>InterfaceDesign</span>
      </div>
    </div>
  );
}

export default Tags;
