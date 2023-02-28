import { useState } from "react";

type dataProps = {
    name: string;
    sub_tree: dataProps[];
}

function Tree({ data }: { data: dataProps}) {
  const [expand, setExpand] = useState(false);
  return (
    <div>
      <span>{data.name}</span>
      <br />
      <div style={{ display:  "block", paddingLeft: 15 }}>
        {data.sub_tree.map((tree) => (
          <Tree key={tree.name} data={tree} />
        ))}
      </div>
    </div>
  );
}

export default Tree;
