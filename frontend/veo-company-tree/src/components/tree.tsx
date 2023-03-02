import { TreeType, TreeSelectedProps } from '../types'

export default function Tree({
  data,
  selectedState,
}: {
  data: TreeType
  selectedState: {
    selected: TreeSelectedProps
    setSelected: (arg0: { id: number; name: string }) => void
  }
}) {
  const { selected, setSelected } = selectedState

  const handleClick = () => {
    setSelected({ id: data.id, name: data.name })
  }
  return (
    <div>
      <button
        className='btn button-light'
        type='button'
        style={{
          margin: '2px',
          border: '1px solid grey',
          borderRadius: '5px',
          backgroundColor: selected.id === data.id ? 'LightSkyBlue' : 'transparent',
        }}
        onClick={handleClick}
      >
        {data.name}
      </button>
      <div style={{ display: 'block', paddingLeft: 20 }}>
        {data.sub_tree?.map((tree) => (
          <Tree key={tree.name} data={tree} selectedState={selectedState} />
        ))}
      </div>
    </div>
  )
}
