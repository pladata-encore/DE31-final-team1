import React from 'react';
import { useDnD } from '@/widgets/layout/flow-dndContext';

import '#/css/flow.css';

const FlowSideinfo = React.forwardRef((props, ref) => {
  const [_, setType] = useDnD();

  const onDragStart = (event, props) => {
    setType(props);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <aside ref={ref}>
      <div className="description">Information of selected node:</div>
      <ul>
        <li>Node ID: {props.id}</li>
        <li>Node Type: {props.type}</li>
        <li>Node Data: {props.data}</li>
        <li>Node Position: {props.position}</li>
      </ul>
    </aside>
  );
});

export default FlowSideinfo;