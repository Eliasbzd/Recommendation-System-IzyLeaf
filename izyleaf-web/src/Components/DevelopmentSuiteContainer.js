import {
  Box,
  Button,
  Center,
  Flex,
  List,
  ListItem,
  Select,
  Skeleton,
  Spacer,
  Text,
  UnorderedList,
  useToast,
} from "@chakra-ui/react";
import { call } from "../lib/call";
import { useEffect, useState } from "react";

import {
  uniqueNamesGenerator,
  adjectives,
  colors,
  animals,
} from "unique-names-generator";

function SessionManagement(props) {
  const { sessionID, updateSession, ...otherProps } = props;
  const toast = useToast();
  const create_session = () => {
    const shortName = uniqueNamesGenerator({
      dictionaries: [adjectives, animals, colors], // colors can be omitted here as not used
      length: 2,
    }); // big-donkey
    call("new_session", { session_name: shortName })
      .then((res) => res.json())
      .then((res) => {
        if (res.success) {
          updateSession(res.session_id);
          toast({
            title: "Created new session",
            description: `Your session id is ${res.session_id}`,
            status: "success",
            duration: 4000,
            isClosable: true,
          });
        } else {
          toast({
            title: "Failed to create new session",
            description: res.error_message,
            status: "error",
            duration: 4000,
            isClosable: true,
          });
        }
      });
  };
  const delete_session = (sessionName) => {
    call("delete_session", { session_name: sessionName })
      .then((res) => res.json())
      .then((res) => {
        if (res.success) {
          toast({
            title: "Removed session",
            description: `removed session named ${sessionName}`,
            status: "success",
            duration: 2000,
            isClosable: true,
          });
          if (sessionID === sessionName) {
            updateSession("None");
          }
          call("get_sessions")
            .then((res) => res.json())
            .then((sess) => setSessionList(sess["sessions"]));
        } else {
          toast({
            title: "Failed to remove session " + sessionName,
            description: res.error_message,
            status: "error",
            duration: 4000,
            isClosable: true,
          });
        }
      });
  };
  const [sessionList, setSessionList] = useState([]);

  return (
    <Box bg="blue.100" {...otherProps}>
      <Flex flexDir="row">
        <Text
          fontWeight="black"
          fontFamily="Open Sans"
          fontSize="xl"
          m="20px"
          width="50%"
        >
          {" "}
          Current Session ID : {sessionID}
        </Text>

        <Button
          rounded="none"
          bg="blue.200"
          width="50%"
          m="20px"
          onClick={create_session}
        >
          Create new IzyLeaf Session
        </Button>
      </Flex>
      <Box width="100%" height="250px">
        <Flex flexDir="row" width="100%" pl="20px" pr="20px">
          <Text fontSize="xl" fontFamily="Open Sans">
            Sessions
          </Text>
          <Spacer width="80%" />
          <Button
            fontFamily="Open Sans"
            rounded="none"
            bg="green.400"
            onClick={() =>
              call("get_sessions")
                .then((res) => res.json())
                .then((sess) => setSessionList(sess["sessions"]))
            }
          >
            Refresh
          </Button>
        </Flex>
        <Box overflow="scroll" height="200px" pb="10px" mt="10px">
          {sessionList === [] ? (
            <Skeleton />
          ) : (
            <List pl="20px" pr="20px" mt="20px">
              {sessionList.map((sessionItem) => (
                <ListItem>
                  <Flex key={sessionItem.session_name}>
                    <Button
                      rounded="none"
                      bg="black"
                      color="white"
                      fontWeight="bold"
                      fontFamily="Open Sans"
                      _hover={{
                        bg: "white",
                        color: "black",
                      }}
                      alignContent="center"
                      width="95%"
                      onClick={() => updateSession(sessionItem.session_name)}
                    >
                      {sessionItem.session_name} (
                      {sessionItem.seen_vehicule_ids.length})
                    </Button>
                    <Button
                      rounded="none"
                      borderColor="black"
                      border="1px"
                      bg="red.400"
                      color="black"
                      fontWeight="bold"
                      fontFamily="Open Sans"
                      _hover={{
                        bg: "white",
                        color: "red.600",
                      }}
                      alignContent="center"
                      width="5%"
                      fontSize="4xl"
                      onClick={() => delete_session(sessionItem.session_name)}
                    >
                      -
                    </Button>
                  </Flex>
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Box>
    </Box>
  );
}

export default function DevelopmentSuiteContainer(props) {
  const {
    updateRecommendation,
    updateSessionID,
    currentSessionID,
    getAnotherRecommendation,
    ...otherProps
  } = props;
  const toast = useToast();

  return (
    <Box {...otherProps}>
      <Center mt="15px">
        <Text fontWeight="bold" fontSize="2xl" fontFamily="Playfair Display">
          IzyLeaf Test Suite
        </Text>
      </Center>
      <SessionManagement
        m="20px"
        width="100%"
        sessionID={currentSessionID}
        updateSession={(newSessionID) => updateSessionID(newSessionID)}
      />
      <Button
        rounded="none"
        bg="blue.200"
        width="100%"
        m="20px"
        onClick={() =>
          call("/reload_vehicule_db")
            .then((res) => res.json())
            .then((res) => {
              if (res.success) {
                toast({
                  title: "Reloaded vehicules",
                  description:
                    "Reloaded the vehicules in the database from the designated file",
                  status: "success",
                  duration: 4000,
                  isClosable: true,
                });
              } else {
                toast({
                  title: "Failed to reload vehicules",
                  description: res.error_message,
                  status: "error",
                  duration: 4000,
                  isClosable: true,
                });
              }
            })
        }
      >
        Reload vehicules database
      </Button>
      <Button
        rounded="none"
        bg="blue.200"
        width="100%"
        m="20px"
        onClick={() => getAnotherRecommendation()}
      >
        Get Recommendation
      </Button>
      <Select placeholder="Select Recommendation Strategy" rounded="none">
        <option value="option1">Select Recommendation Strategy</option>
      </Select>
    </Box>
  );
}
