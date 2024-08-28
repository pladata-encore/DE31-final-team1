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
import Flow from "@/widgets/cards/flow";

import "@xyflow/react/dist/style.css";

export function Rules() {
  
  return (
    <Flow width="100%" height="86vh" />
  );
}

export default Rules;
