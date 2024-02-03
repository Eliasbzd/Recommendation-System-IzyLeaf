import {
  Box,
  Button,
  Center,
  ChakraProvider,
  Flex,
  Grid,
  GridItem,
  Image,
  Spacer,
  Text,
  useToast,
} from "@chakra-ui/react";
import theme from "./lib/theme";
import SwipeComponent from "./Components/SwipeComponent";
import DevelopmentSuiteContainer from "./Components/DevelopmentSuiteContainer";
import { useState } from "react";
import { call } from "./lib/call";

function App() {
  const toast = useToast();

  const [currentRecommendedVehicule, setCurrentRecommendedVehicule] = useState(
    {}
  );
  const [currentSessionID, setCurrentSessionID] = useState(null);
  const getNextRecommendation = () => {
    call("get_recommendation", {
      session_id: currentSessionID,
      recommendation_strategy: "base_recommendation2",
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        if (res["success"]) {
          setCurrentRecommendedVehicule(JSON.parse(res["recommendation"]));
        } else {
          toast({
            title: "Failed to recommend a vehicule",
            description: "",
            status: "error",
            duration: 4000,
            isClosable: true,
          });
        }
      });
  };

  return (
    <ChakraProvider theme={theme}>
      <Flex flexDirection="row">
        <Box width="49%" height="100vh">
          <DevelopmentSuiteContainer
            updateRecommendation={setCurrentRecommendedVehicule}
            updateSessionID={setCurrentSessionID}
            currentSessionID={currentSessionID}
            getAnotherRecommendation={getNextRecommendation}
          />
        </Box>
        <Spacer />
        <Box width="49%" height="95vh" bgColor="gray.100">
          <SwipeComponent
            recVeh={currentRecommendedVehicule}
            sessionID={currentSessionID}
            getNextRecommendation={getNextRecommendation}
            height="100%"
          />
        </Box>
      </Flex>
    </ChakraProvider>
  );
}

export default App;
