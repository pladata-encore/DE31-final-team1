import React, { useState, useCallback, useRef, useEffect } from 'react';
import {
  ReactFlow,
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  useReactFlow,
  Background,
} from '@xyflow/react';
import FlowSidenav from '@/widgets/layout/flow-sidenav';
import { DnDProvider, useDnD } from '@/widgets/layout/flow-dndContext'
import FlowSideinfo from '@/widgets/layout/flow-sideinfo';
import axios from 'axios';

// import test data
import { ruleTestData } from '@/data';


import '@xyflow/react/dist/style.css';
import '#/css/flow.css';

const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: { label: 'input node' },
    position: { x: 250, y: 5 },
  },
];

let id = 0;
const getId = () => `dndnode_${id++}`;

// Start Widget
export const Flow = ({width, height}) => {
  // Start Widget Variables
  const reactFlowWrapper = useRef(null);
  const nodeInfoRef = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { screenToFlowPosition } = useReactFlow();
  const [type] = useDnD();
  let isInit = false;
  // End Widget Variables

  // Start Widget Functions
  useEffect(() => { // get flow data when the widget is loaded, only once
    if (!isInit) {
      getFlowInfo();
      isInit = !isInit;
    }
  }, []);

  const getFlowInfo = () => {
    // axios.get('http://localhost:5000/flow') // in production use API to get flow data
    // in development use test data
    const jsonFlow = ruleTestData;
    console.log(jsonFlow);
    jsonToFlow(jsonFlow);
  }

  const jsonToFlow = (data) => {
    data.processors.forEach((processor) => {
      const modifiedPosition = {
        x: processor.Position.x/2,
        y: processor.Position.y/2,
      };
      const newNode = {
        id: processor.ID,
        // type: processor.Type, // type is not defined in the test data
        type: 'default', // so use default type
        position: modifiedPosition,
        data: { label: processor.Name },
      };
      setNodes((nds) => nds.concat(newNode));
    }
    );
    data.connections.forEach((connection) => {
      const newEdge = {
        id: connection['Connection ID'],
        source: connection['Source Processor ID'],
        target: connection['Destination Processor ID'],
        type: 'step',
      };
      setEdges((eds) => eds.concat(newEdge));
    }
    );
  }

  const onConnect = useCallback(
    // set edges as step style
    (params) => setEdges((eds) => addEdge({ ...params, type: 'step' }, eds)),
    [],
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      // check if the dropped element is valid
      if (!type) {
        return;
      }

      // project was renamed to screenToFlowPosition
      // and you don't need to subtract the reactFlowBounds.left/top anymore
      // details: https://reactflow.dev/whats-new/2023-11-10
      const position = screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      const newNode = {
        id: getId(),
        type,
        position,
        data: { label: `${type} node` },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [screenToFlowPosition, type],
  );

  const onNodeClickEvent = (event, node) => {
    console.log('click', node, event);
    console.log(nodeInfoRef.current);

    // change the info of nodeInfoRef with the clicked node
    nodeInfoRef.current.innerHTML = `
      <div class="description">Information of selected node:</div>
      <ul>
        <li>Node ID: ${node.id}</li>
        <li>Node Type: ${node.type}</li>
        <li>Node Data: ${node.data.label}</li>
        <li>Node Position: x: ${node.position.x}, y: ${node.position.y}</li>
      </ul>
    `;
    // redraw the nodeInfoRef
    nodeInfoRef.current.style.display = 'block';
  };
  // End Widget Functions

  return (
    <div className="dndflow" style={{ width, height, display:'flex' }}>
      <FlowSidenav style={{ width }} />
      <div className="reactflow-wrapper" ref={reactFlowWrapper} style={{ width, height }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onNodeClick={(event, node) => onNodeClickEvent(event, node)}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      {/* Warning: Function components cannot be given refs. Attempts to access this ref will fail. Did you mean to use React.forwardRef()? */}
      <FlowSideinfo ref={nodeInfoRef}
      id='' type='' data='' position='' />
    </div>
  );
}
// End Widget

export default () => (
  <ReactFlowProvider>
    <DnDProvider>
      <Flow width="100%" height="86vh" />
    </DnDProvider>
  </ReactFlowProvider>
)
