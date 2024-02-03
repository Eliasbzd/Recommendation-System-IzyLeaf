import {
  Box,
  Button,
  Center,
  Grid,
  GridItem,
  Image,
  Spacer,
  Text,
  useToast,
} from "@chakra-ui/react";

import { useState } from "react";
import { call } from "../lib/call";

function CarInfo(props) {
  const { recVeh, ...otherProps } = props;

  return (
    <Box {...otherProps}>
      <Image height="60%" m="20px" src={recVeh["vehiculeImageURL"]} />
      <Box height="30%">
        <Center height="100%" width="100%">
          <Grid
            w="100%"
            h="100%"
            templateRows="repeat(3, 1fr)"
            templateColumns="repeat(5, 1fr)"
            gap={4}
            fontFamily="Open Sans"
            m="12px"
            p="10px"
            bgColor="whiteAlpha.600"
          >
            <GridItem colSpan={1}>
              <Text fontWeight="bold">BRAND : </Text> {recVeh["brand"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">MODEL : </Text> {recVeh["model"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">YEAR : </Text> {recVeh["year"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">DEALER : </Text> {recVeh["dealer"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">COLOR : </Text> {recVeh["color"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">DISTANCE : </Text> {recVeh["km"]} km
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">FUEL : </Text> {recVeh["fuel"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">GEARBOX : </Text> {recVeh["gearbox"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">DOORS : </Text> {recVeh["doors"]}
            </GridItem>
            <GridItem colSpan={1}>
              <Text fontWeight="bold">SEATS : </Text> {recVeh["seats"]}
            </GridItem>
            <GridItem colSpan={5}>
              <Center>{recVeh["price"]}</Center>
            </GridItem>
          </Grid>
        </Center>
      </Box>
    </Box>
  );
}

export default function SwipeComponent(props) {
  const { recVeh, sessionID, getNextRecommendation, ...otherProps } = props;
  const toast = useToast();

  const interactWithRecommendation = (interaction) => {
    call("interact_with_rec", {
      session_id: sessionID,
      vehicule_id: recVeh["id"],
      reaction: interaction,
    })
      .then((res) => res.json())
      .then((res) => {
        if (res["success"]) {
          getNextRecommendation();
        } else {
          toast({
            title: "Failed to take interaction into consideration",
            description: "",
            status: "error",
            duration: 4000,
            isClosable: true,
          });
        }
      });
  };

  console.log(recVeh);
  return (
    <Box {...otherProps}>
      {recVeh === {} ? (
        <>GET AN INITIAL RECOMMENDATION TO START</>
      ) : (
        <CarInfo recVeh={recVeh} width="100%" height="100%" />
      )}

      <Box width="100%" height="10%">
        <Button
          bgColor="red.400"
          width="50%"
          height="100%"
          rounded="none"
          onClick={() => interactWithRecommendation(0)} //React rehydration somehow makes this get executed twice ... Need to fix that, maybe a timer in call that starts when same params or look for potential problems in ui code
        >
          NAY
        </Button>
        <Button
          bgColor="green.400"
          width="50%"
          height="100%"
          rounded="none"
          onClick={() => interactWithRecommendation(1)}
        >
          YAY
        </Button>
      </Box>
    </Box>
  );
}
