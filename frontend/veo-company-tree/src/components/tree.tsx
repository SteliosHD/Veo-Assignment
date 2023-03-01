import { useEffect, useRef } from "react";

type dataProps = {
    name: string;
    id: number;
    sub_tree: dataProps[];
}

export default function Tree({
  data,
  selectedState,
}: {
  data: dataProps;
  selectedState: { selected: { id: number; name: string }; setSelected: (arg0: { id: number; name: string }) => void };
}) {
  const { selected, setSelected } = selectedState;

  const handleClick = () => {
    setSelected({ id: data.id, name: data.name });
  };

  useEffect(() => {
    if (selected.id === data.id) {
      console.log("selected");
      console.log(selected.id, selected.name);
    }
  }, [selected, data.id, , setSelected]);


  
  return (
    <div>
      <button
        className="btn button-light"
        style={{
          margin: "2px",
          border: "1px solid grey",
          borderRadius: "5px",
          backgroundColor:
            selected.id === data.id ? "LightSkyBlue" : "transparent",
        }}
        onClick={handleClick}
      >
        {data.name}
      </button >
      <div style={{ display: "block", paddingLeft: 20 }}>
        {data.sub_tree.map((tree) => (
          <Tree key={tree.name} data={tree} selectedState={selectedState} />
        ))}
      </div>
    </div>
  );
}

