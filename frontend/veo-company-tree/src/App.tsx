import Tree from "./components/tree";
// eslint-disable-next-line import/no-unresolved
import tree_json from "./Data/tree_outputs";

export default function App() {
  return (
    <div className="App">
      <Tree data={tree_json.trees[0]} />
    </div>
  );
}