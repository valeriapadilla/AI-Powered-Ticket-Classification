type TabHeaderProps = {
  tabs: string[]
  activeTab: number
  onTabChange: (index: number) => void
}

export default function TabHeader({ tabs, activeTab, onTabChange }: TabHeaderProps) {
  return (
    <div className="border-b border-gray-200 mb-4 overflow-x-auto">
      <div className="flex min-w-[300px]">
        {tabs.map((tab, idx) => (
          <button
            key={tab}
            onClick={() => onTabChange(idx)}
            className={`
              flex-1 min-w-[100px]
              text-center
              pb-2 text-lg font-medium
              whitespace-nowrap
              ${
                activeTab === idx
                  ? 'border-b-2 border-primary text-primary'
                  : 'text-gray-500 hover:text-primary'
              }
            `}
          >
            {tab}
          </button>
        ))}
      </div>
    </div>
  )
}
