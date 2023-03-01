import Tree from "./components/tree";
import { useState } from "react";


import tree_json from "./Data/tree_outputs";
import Form from "./components/form";

export type selectedProps = {
  id: number;
  name: string;
};

export default function App() {
  const [selected , setSelected]  = useState<selectedProps>({id:-1, name:"None"});

  
  
  return (
    <>
      <nav
        className="navbar navbar-light"
        style={{ backgroundColor: "#e3f2fd", marginBottom:"20px"}}
      >
        <div className="container">
          <a className="navbar-brand" href="/">
            <img src={process.env.PUBLIC_URL + "/logo.png"} alt="" width="50" />{" "}
            Veo Assignment
          </a>
        </div>
      </nav>
      <div
        className="App container"
      >
        <div className="row">
          <div className="col-6">
            <h1>Company Structure</h1>
            <Tree
              data={tree_json.trees[0]}
              selectedState={{ selected, setSelected }}
            />
          </div>
          <div className="wrapper col-6">
            <h2>Create a child node</h2>
            <div style={{ color: "black" }}>
              <h5 style={{ color: "gray" }}>
                Selected Parent Node:{" "}
                <span style={{ fontWeight: "600", color: "lightskyblue" }}>
                  {selected.id !== -1 ? selected.name : "None"}
                </span>
              </h5>
            </div>
            <Form selected={selected} />
          </div>
        </div>
      </div>
    </>
  );
}