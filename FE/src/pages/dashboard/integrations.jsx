import {
  Button,
  Card,
  CardHeader,
  CardBody,
  Typography,
  Avatar,
  Chip,
  Tooltip,
  Progress,
} from "@material-tailwind/react";
import axios from "axios";
import React from "react";
import { EllipsisVerticalIcon } from "@heroicons/react/24/outline";
import { farmTableData } from "@/data";
import { DsSelModal } from "@/widgets/layout";

export function Integrations() {
  const [dsList, setDsList] = React.useState([]);
  const cookies = document.cookie.split(";").reduce((acc, cookie) => {
    const [key, value] = cookie.split("=").map(part => part.trim());
    acc[key] = value;
    return acc;
  }, {});

  function dataPopup() {
    document.getElementById("dataPopup").classList.toggle("hidden");
  }

  React.useEffect(() => {
    axios.get("http://192.168.1.230:19020/v1/data-source/getdslist", {
      params: {
        email: cookies.userEmail,
        token: cookies.userAuth,
      },
    }).then((res) => {
      console.log(res);
      setDsList(res.data);
    }).catch((err) => {
      console.log(err);
    });
  }, []);

  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      {/* make data popup covering full page */}
      <DsSelModal />
      <Card>
        <CardHeader variant="gradient" color="gray" className="mb-6 p-6">
          <Typography variant="h6" color="white">
            Data Source List
          </Typography>
        </CardHeader>
        <Button
          variant="text"
          color="blue-gray"
          className="flex items-center border border-blue-gray-200 p-2 rounded-lg mr-4 mb-2"
          style={{ marginLeft: "auto" }}
          onClick={dataPopup}
        >
          <Typography variant="h6" color="black" className="font-semibold">
            Add Data Source
          </Typography>
        </Button>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <table className="w-full min-w-[640px] table-auto">
            <thead>
              <tr>
                {["num", "name", "location", "type", "status", "date", ""].map((el) => (
                  <th
                    key={el}
                    className="border-b border-blue-gray-50 py-3  px-5 text-left"
                  >
                    <Typography
                      variant="small"
                      className="text-[11px] font-bold uppercase text-blue-gray-400"
                    >
                      {el}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {farmTableData.map(
                ({ num, name, location, type, online, date }, key) => {
                  const className = `py-3 px-5 ${
                    key === farmTableData.length - 1
                      ? ""
                      : "border-b border-blue-gray-50"
                  }`;

                  return (
                    <tr key={num}>
                      <td className={className}>
                        <Typography className="text-xs font-semibold text-blue-gray-600">
                          {num}
                        </Typography>
                      </td>
                      <td className={className}>
                        <div className="flex items-center gap-4">
                          {/* <Avatar src={img} alt={name} size="sm" variant="rounded" /> */}
                          <div>
                            <Typography
                              variant="small"
                              color="blue-gray"
                              className="font-semibold"
                            >
                              {name}
                            </Typography>
                          </div>
                        </div>
                      </td>
                      <td className={className}>
                        <Typography className="text-xs font-semibold text-blue-gray-600">
                          {location}
                        </Typography>
                      </td>
                      <td className={className}>
                        <Typography className="text-xs font-semibold text-blue-gray-600">
                          {type}
                        </Typography>
                        <Typography className="text-xs font-normal text-blue-gray-500">
                          {type}
                        </Typography>
                      </td>
                      <td className={className}>
                        <Chip
                          variant="gradient"
                          color={online ? "green" : "blue-gray"}
                          value={online ? "online" : "offline"}
                          className="py-0.5 px-2 text-[11px] font-medium w-fit"
                        />
                      </td>
                      <td className={className}>
                        <Typography className="text-xs font-semibold text-blue-gray-600">
                          {date}
                        </Typography>
                      </td>
                      <td className={className}>
                        <Typography
                          as="a"
                          href="#"
                          className="text-xs font-semibold text-blue-gray-600"
                        >
                          Edit
                        </Typography>
                      </td>
                    </tr>
                  );
                }
              )}
            </tbody>
          </table>
        </CardBody>
      </Card>
      {/* <Card>
        <CardHeader variant="gradient" color="gray" className="mb-8 p-6">
          <Typography variant="h6" color="white">
            Projects Table
          </Typography>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <table className="w-full min-w-[640px] table-auto">
            <thead>
              <tr>
                {["companies", "members", "budget", "completion", ""].map(
                  (el) => (
                    <th
                      key={el}
                      className="border-b border-blue-gray-50 py-3 px-5 text-left"
                    >
                      <Typography
                        variant="small"
                        className="text-[11px] font-bold uppercase text-blue-gray-400"
                      >
                        {el}
                      </Typography>
                    </th>
                  )
                )}
              </tr>
            </thead>
            <tbody>
              {projectsTableData.map(
                ({ img, name, members, budget, completion }, key) => {
                  const className = `py-3 px-5 ${
                    key === projectsTableData.length - 1
                      ? ""
                      : "border-b border-blue-gray-50"
                  }`;

                  return (
                    <tr key={name}>
                      <td className={className}>
                        <div className="flex items-center gap-4">
                          <Avatar src={img} alt={name} size="sm" />
                          <Typography
                            variant="small"
                            color="blue-gray"
                            className="font-bold"
                          >
                            {name}
                          </Typography>
                        </div>
                      </td>
                      <td className={className}>
                        {members.map(({ img, name }, key) => (
                          <Tooltip key={name} content={name}>
                            <Avatar
                              src={img}
                              alt={name}
                              size="xs"
                              variant="circular"
                              className={`cursor-pointer border-2 border-white ${
                                key === 0 ? "" : "-ml-2.5"
                              }`}
                            />
                          </Tooltip>
                        ))}
                      </td>
                      <td className={className}>
                        <Typography
                          variant="small"
                          className="text-xs font-medium text-blue-gray-600"
                        >
                          {budget}
                        </Typography>
                      </td>
                      <td className={className}>
                        <div className="w-10/12">
                          <Typography
                            variant="small"
                            className="mb-1 block text-xs font-medium text-blue-gray-600"
                          >
                            {completion}%
                          </Typography>
                          <Progress
                            value={completion}
                            variant="gradient"
                            color={completion === 100 ? "green" : "gray"}
                            className="h-1"
                          />
                        </div>
                      </td>
                      <td className={className}>
                        <Typography
                          as="a"
                          href="#"
                          className="text-xs font-semibold text-blue-gray-600"
                        >
                          <EllipsisVerticalIcon
                            strokeWidth={2}
                            className="h-5 w-5 text-inherit"
                          />
                        </Typography>
                      </td>
                    </tr>
                  );
                }
              )}
            </tbody>
          </table>
        </CardBody>
      </Card> */}
    </div>
  );
}

export default Integrations;
