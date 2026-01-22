import Skeleton from './Skeleton';

export function CardSkeleton() {
  return (
    <div className="bg-white dark:bg-dark-secondary rounded-xl overflow-hidden border border-gray-100 dark:border-gray-800 shadow-sm">
      {/* Image placeholder */}
      <Skeleton className="w-full h-48" />

      <div className="p-4 space-y-3">
        {/* Meta tags */}
        <div className="flex gap-2">
          <Skeleton className="h-6 w-20 rounded-full" />
          <Skeleton className="h-6 w-16 rounded-full" />
        </div>

        {/* Title */}
        <Skeleton className="h-6 w-3/4" />

        {/* Description lines */}
        <div className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
        </div>

        {/* Footer/Author */}
        <div className="flex items-center gap-3 pt-2">
          <Skeleton className="h-8 w-8 rounded-full" />
          <div className="space-y-1">
            <Skeleton className="h-3 w-24" />
            <Skeleton className="h-3 w-16" />
          </div>
        </div>
      </div>
    </div>
  );
}

interface SectionSkeletonProps {
  marginTop?: number;
}

export function SectionSkeleton({ marginTop = 4 }: SectionSkeletonProps) {
  return (
    <section
      className={`lg:mt-4 max-w-7xl mx-auto px-4 lg:px-8 mb-4 mt-${marginTop}`}
    >
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div className="my-4">
          <Skeleton className="h-8 w-48 mb-2" />
          <Skeleton className="h-1 w-20" />
        </div>
        <Skeleton className="h-6 w-16" />
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <CardSkeleton key={i} />
        ))}
      </div>
    </section>
  );
}
