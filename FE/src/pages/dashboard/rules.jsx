import {
  Card,
  CardHeader,
  CardBody,
  Typography,
  Avatar,
  Chip,
  Tooltip,
  Progress,
  Button,
} from "@material-tailwind/react";
import { EllipsisVerticalIcon } from "@heroicons/react/24/outline";
import { ruleTableData } from "@/data";
import { ReactFlow } from "@xyflow/react"

import "@xyflow/react/dist/style.css";

export function Rules() {
  const initialNodes = [
    {
      id: '1',
      type: 'input',
      data: { label: 'Input Node' },
      position: { x: 0, y: 0 },
    },
    {
      id: '2',
      type: 'output',
      data: { label: <div>Output Node</div> },
      position: { x: 100, y: 100 },
    }
  ];
  const initialEdges = [
    { id: 'e1-2', source: '1', target: '2', animated: true },
    { id: 'e2-3', source: '2', target: '3', animated: true },
  ];
  
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow elements={initialNodes} style={{zIndex:"99"}} />
    </div>
  );
}

export default Rules;
