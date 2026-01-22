import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { GoArrowDownRight, GoArrowUpRight } from 'react-icons/go';
import Text from '../../../components/common/Text';
import { useDashboardMetrics } from '../hooks/useAnalytics';
import { useState } from 'react';
import Spinner from '../../../components/common/Spinner';

function Analytics() {
  const [period, setPeriod] = useState<'weekly' | 'monthly'>('weekly');
  const { data, isLoading, error } = useDashboardMetrics(period);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-[500px]">
        <Spinner />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex justify-center items-center h-[500px] text-red-500">
        Failed to load analytics data
      </div>
    );
  }

  const deviceTypesData = data.device_types.map((d) => ({
    name: d.name,
    value: d.value,
    color:
      d.name === 'Mobile'
        ? '#a32816'
        : d.name === 'Tablet'
        ? '#F58F29'
        : '#2EA316',
  }));

  const activeUsersData = data.active_users.map((d) => ({
    name: d.day,
    registered: d.registered_users,
    visitors: d.visitors,
    total: d.total_active_users,
  }));

  // Aggregate top posts by category from the API response
  const topPerformingPostsData = Object.entries(data.top_performing_posts).map(
    ([category, posts]) => ({
      category: category.charAt(0).toUpperCase() + category.slice(1),
      views: posts.reduce((sum, p) => sum + p.views, 0),
      shares: 0, // Shares not currently in TopPost interface, would need API update or mock
    })
  );

  const { metrics } = data;

  return (
    <div className="flex flex-col gap-4 px-2 lg:px-0">
      <div className="flex lg:flex-row flex-col justify-between gap-4">
        <div className="flex flex-2 flex-col gap-4">
          <div className="my-6 lg:my-0 flex flex-col lg:flex-row gap-4 justify-between text-primary dark:text-custom-white">
            <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
              <span className="text-sm">Time on page</span>
              <span className="font-semibold text-2xl">
                {(metrics.avg_session_duration.value / 60).toFixed(1)} min
              </span>
              <p className="inline-flex items-center gap-2 text-xs">
                <span>
                  {metrics.avg_session_duration.trend === 'up' ? (
                    <GoArrowUpRight className="text-lime-green" />
                  ) : (
                    <GoArrowDownRight className="text-red" />
                  )}
                </span>
                <span>
                  {metrics.avg_session_duration.change > 0 ? '+' : ''}
                  {metrics.avg_session_duration.change}% this {period}
                </span>
              </p>
            </div>
            <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
              <span className="text-sm">Bounce rate</span>
              <span className="font-semibold text-2xl">
                {metrics.bounce_rate.value}%
              </span>
              <p className="inline-flex items-center gap-2 text-xs">
                <span>
                  {metrics.bounce_rate.trend === 'down' ? (
                    <GoArrowDownRight className="text-lime-green" />
                  ) : (
                    <GoArrowUpRight className="text-red" />
                  )}
                </span>
                <span>
                  {metrics.bounce_rate.change > 0 ? '+' : ''}
                  {metrics.bounce_rate.change}% this {period}
                </span>
              </p>
            </div>
            <div className="flex flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
              <span className="text-sm">Load speed</span>
              <span className="font-semibold text-2xl">
                {metrics.page_load_time.value} ms
              </span>
              <p className="inline-flex items-center gap-2 text-xs">
                <span>
                  {metrics.page_load_time.trend === 'down' ? (
                    <GoArrowDownRight className="text-lime-green" />
                  ) : (
                    <GoArrowUpRight className="text-red" />
                  )}
                </span>
                <span>
                  {metrics.page_load_time.change > 0 ? '+' : ''}
                  {metrics.page_load_time.change}% this {period}
                </span>
              </p>
            </div>
          </div>
          <div className="flex h-full justify-center flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
            <div className="flex justify-between w-full">
              <h3>Top Hashtag Performance</h3>
              <p>...</p>
            </div>
            <div className="flex justify-between w-full">
              <div className="flex">
                <p className="text-cyan-light">#</p>
                <h3>Crypto</h3>
              </div>
              <p>1.5k Engagements</p>
            </div>
          </div>
        </div>
        <div className="flex flex-1 flex-col items-center gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
          <div className="flex justify-between gap-4">
            <Text
              variant="h3"
              bold={false}
              className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
            >
              Device types
            </Text>

            <form>
              <select
                className="dark:text-custom-white dark:bg-dark text-sm py-1 px-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700"
                value={period}
                onChange={(e) =>
                  setPeriod(e.target.value as 'weekly' | 'monthly')
                }
              >
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </form>
          </div>
          {/* Width and height has to be set on a div for the piechart to display */}
          <div className="w-full h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={deviceTypesData}
                  nameKey="name" // property e.g Mobile
                  dataKey="value" // value: 400
                  innerRadius="40%" // creates a donut hole
                  outerRadius="70%" // sets the outer boundary
                  cx="50%" // cx and cy centres the pie chart
                  cy="50%"
                  paddingAngle={3} // Adds a 3-degree gap between slices
                >
                  {deviceTypesData.map((entry) => (
                    <Cell
                      fill={entry.color} // Sets the fill color for each slice
                      stroke={entry.color} // Sets the border color for each slice
                      key={entry.value}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend
                  verticalAlign="bottom"
                  align="center"
                  layout="horizontal"
                  iconSize={15}
                  iconType="circle"
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <div className="flex flex-col lg:flex-row gap-4">
        <div className="flex flex-1 flex-col gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
          <div className="flex justify-between">
            <Text
              variant="h3"
              bold={false}
              className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
            >
              Active users overview
            </Text>
            <form>
              <select
                className="dark:text-custom-white text-sm dark:bg-dark py-1 px-2  border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700"
                value={period}
                onChange={(e) =>
                  setPeriod(e.target.value as 'weekly' | 'monthly')
                }
              >
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </form>
          </div>
          <div className="w-full h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              {/* creates space around the chart for axes and labels */}
              <LineChart
                data={activeUsersData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                {/* Creates the background grid lines with a dash pattern and light opacity */}
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="name" /> {/* Displays days of the week */}
                {/* Automatically scales to fit your data values (450 to 2250) */}
                <YAxis />
                <Tooltip />
                <Legend
                  verticalAlign="bottom"
                  align="center"
                  layout="horizontal"
                  iconSize={15}
                  iconType="circle"
                  formatter={(value) => {
                    // Map data keys to custom labels
                    const customLabels: { [key: string]: string } = {
                      registered: 'Registered Users',
                      visitors: 'Visitors',
                      total: 'Total Active Users',
                    };

                    // Return the custom label if it exists, otherwise return the original value
                    return (
                      <span className="text-xs lg:text-sm">
                        {customLabels[value] || value}
                      </span>
                    );
                  }}
                />
                <Line
                  type="monotone" // creates smooth, curved lines between points
                  dataKey="registered"
                  stroke="#a32816" // Sets the line color (using your theme colors)
                  strokeWidth={2} // Makes the lines thicker for better visibility
                  activeDot={{ r: 8 }} // makes the active dot larger when hovering
                />
                <Line
                  type="monotone"
                  dataKey="visitors"
                  stroke="#F58F29"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="total"
                  stroke="#2EA316"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="flex flex-col flex-1 gap-y-5 px-8 py-3 rounded-md border border-primary dark:border-gray-200">
          <div className="flex justify-between">
            <Text
              variant="h3"
              bold={false}
              className="font-semibold mb-1 text-gray-900 dark:text-custom-white"
            >
              Top Performing Post
            </Text>
            <form>
              <select
                className="dark:text-custom-white text-sm dark:bg-dark py-1 px-2  border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus:ring-gray-700"
                value={period}
                onChange={(e) =>
                  setPeriod(e.target.value as 'weekly' | 'monthly')
                }
              >
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </form>
          </div>

          <div className="w-full h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={topPerformingPostsData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="category" />
                <YAxis domain={[0, 3000]} />
                <Tooltip />
                <Legend
                  verticalAlign="bottom"
                  align="center"
                  layout="horizontal"
                  iconSize={15}
                  iconType="circle"
                />
                <Bar dataKey="views" name="Views" fill="#a32816" barSize={30} />
                <Bar
                  dataKey="shares"
                  name="Shares"
                  fill="#F58F29"
                  barSize={30}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Analytics;
