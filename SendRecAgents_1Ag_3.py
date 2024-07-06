# import os
# import shutil
import math
import neat
import visualize
import matplotlib.pyplot as plt

import random
# import matplotlib.pyplot as plt
import turtle
import VizualizerClass

import multiprocessing
import os
import pickle
import functools

import ParallelEvaluatorMod
import PopulationMod
import time
from PIL import Image, ImageDraw
import io

import glob

generation_counter = [0]

TimeLimit=100
TimeFitness=20  # The last steps measured for fitness
MaxSpeed=math.pi/9
RunsPerTrial = 3
Verbose = False
genVerb = 30
NUM_GENERATIONS = 300

receiver=0 #pos in pi
sender=0

#Food area variables
foodPos = math.pi
foodPoss = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
foodAreaId = 0 #[0,1,2,3,4]
foodSize = math.pi/4

#Turtle graphics variables
CircleRadius=50
# turt=turtle.Turtle
agentVisuals = VizualizerClass.agentEnvironment(radius=100)
gifGranularity=5

def get_input(agent): #Gets position
    """Gets positions in cos() sin

    Args:
        agent (float): The angular position measured in pi [-pi, pi]

    Returns:
        float: cos(agent)
        float: sin(agent)
    """
    return (math.cos(agent),math.sin(agent))

def advancePos(agent,speedLeft,speedRight): #Returns the new angle of agent, only update every step
    """Returns the angular position (radians) of the agent at the next time step

    Args:
        agent (float): Angular position
        speedLeft (float): [-MaxSpeed to MaxSpeed]
        speedRight (float): [-MaxSpeed to MaxSpeed]

    Returns:
        float: New angular position of agent in radians 
    """
    speedLeft = abs(speedLeft * math.pi/9); speedRight = abs(speedRight * math.pi/9)
    if speedLeft > MaxSpeed: speedLeft = MaxSpeed
    if speedRight > MaxSpeed: speedRight = MaxSpeed
    angVel = speedRight - speedLeft
    angVel = max(-MaxSpeed, min(MaxSpeed, angVel)) #Clamp values
    newAngle = agent + angVel
    if newAngle > math.pi:
        newAngle = newAngle - 2*math.pi
    elif newAngle < - math.pi:
        newAngle = newAngle + 2*math.pi
    return newAngle # o angulo novo do agente)
            
def one_step(receiver,act_receiver):
    """Returns an advancement of positions of 1 agent

    Returns an advancement of angular positions in radians of 2 agents

    Args:
        receiver
        act_receiver (tuple of 2 floats [0,1]): speed left

    Returns:
        _type_: _description_
    """
    act1_receiver,act2_receiver = act_receiver

    return advancePos(receiver,act1_receiver,act2_receiver)

def pair_step(sender,receiver,act_sender,act_receiver):
    """Returns an advancement of positions of 2 agents

    Returns an advancement of angular positions in radians of 2 agents

    Args:
        sender
        receiver
        act_sender (tuple of 2 floats [0,1]): speed right
        act_receiver (tuple of 2 floats [0,1]): speed left

    Returns:
        _type_: _description_
    """
    act1_sender,act2_sender = act_sender
    act1_receiver,act2_receiver = act_receiver

    return advancePos(sender,act1_sender,act2_sender),advancePos(receiver,act1_receiver,act2_receiver)
               
# act_sender,act_receiver=calc_actions()              
# sender,receiver=pair_step(senderPos1,senderPos2,receiver,act_sender,act_receiver)

fitness_area=(math.pi/4,math.pi/2)

def orderNum(num):
    numStr = str(num)
    remaindingZeros = 3 - len(numStr)
    for i in range(remaindingZeros):
        numStr = "".join(["0",numStr])
    return numStr

#region deleteProb
def eval_fitness(circRad, verbose=Verbose):
    count=0
    time=0
    receiver=sender=0

    #Create turtle visuals
    if verbose:
        # display(time,sender,receiver)
        print("time: "+str(time)+"\nSender (pos): "+str(sender)+"\nReceiver (pos): "+str(receiver))

        #region createVisualTurtles
        turtleSend = turtle.Turtle()
        turtleRec = turtle.Turtle()
        turtleRec.fillcolor("green"), turtleSend.fillcolor("violet")
        turtleSend.shape("circle"), turtleRec.shape("circle")
        turtleSend.shapesize(0.4, 0.4), turtleRec.shapesize(0.4, 0.4)
        turtleSend.penup(), turtleRec.penup()
        turtleSend.speed(0), turtleRec.speed(0)
        #endregion

    for t in range(TimeLimit):
        act_sender=random.random()*MaxSpeed,random.random()*MaxSpeed
        act_receiver=random.random()*MaxSpeed,random.random()*MaxSpeed
        sender,receiver=pair_step(sender,receiver,act_sender,act_receiver)
        if(verbose): #Change turtle graphic positions
            pos = anglePosition2(sender, circRad)
            turtleSend.goto(pos)
            pos = anglePosition2(receiver, circRad)
            turtleRec.goto(pos)
        # recebe genoma
        # cria rede
        # activa a rede com os inputs dos agentes
        # recolhe os outputs e faz os advances
        #

        # if sender est+a na fitness area e instante de fitness:
        if t > TimeLimit-TimeFitness:
            if sender >= foodPos-foodSize/2 or sender <= -(foodPos-foodSize/2):
                count+=1
            if verbose:
                print("time: "+str(t)+"\nSender (pos): "+str(sender)+"\nReceiver (pos): "+str(receiver))
    return count/TimeFitness

def eval_fitness2(circRad, act_sender, act_receiver, verbose=Verbose):
    count=0
    time=0
    receiver=sender=0

    #Create turtle visuals
    if verbose:
        # display(time,sender,receiver)
        print("time: "+str(time)+"\nSender (pos): "+str(sender)+"\nReceiver (pos): "+str(receiver))

        #region createVisualTurtles
        turtleSend = turtle.Turtle()
        turtleRec = turtle.Turtle()
        turtleRec.fillcolor("green"), turtleSend.fillcolor("violet")
        turtleSend.shape("circle"), turtleRec.shape("circle")
        turtleSend.shapesize(0.4, 0.4), turtleRec.shapesize(0.4, 0.4)
        turtleSend.penup(), turtleRec.penup()
        turtleSend.speed(0), turtleRec.speed(0)
        #endregion

    for t in range(TimeLimit):
        # act_sender=random.random()*MaxSpeed,random.random()*MaxSpeed
        act_sender1, act_sender2 = act_sender
        act_sender=act_sender1*MaxSpeed,act_sender2*MaxSpeed
        act_receiver1, act_receiver2 = act_receiver
        act_receiver=act_receiver1*MaxSpeed,act_receiver2*MaxSpeed
        sender,receiver=pair_step(sender,receiver,act_sender,act_receiver)
        if(verbose): #Change turtle graphic positions
            pos = anglePosition2(sender, circRad)
            turtleSend.goto(pos)
            pos = anglePosition2(receiver, circRad)
            turtleRec.goto(pos)
        # recebe genoma
        # cria rede
        # activa a rede com os inputs dos agentes
        # recolhe os outputs e faz os advances
        #

        # if sender est+a na fitness area e instante de fitness:
        if t > TimeLimit-TimeFitness:
            if sender >= foodPos-foodSize/2 or sender <= -(foodPos-foodSize/2):
                count+=1
            if verbose:
                print("time: "+str(t)+"\nSender (pos): "+str(sender)+"\nReceiver (pos): "+str(receiver))
    return count/TimeFitness
#endregion

def anglePosition2(angle, rad):
    """Returns the absolute position of an angle in an circumference with an offset in y (x, y+offset)

    Args:
        angle (float): radians
        rad (float): radius

    Returns:
        float, float: posX, posY + rad
    """
    x, y = rad*math.cos(angle),rad*math.sin(angle)
    return x, y + rad

def getAngleRadians(sinX, cosX):
    return math.atan(sinX/cosX)

def drawCircle(rad, turt, fitnessZone):
    """_summary_

    Args:
        rad (float): radius of the circle
        turt (Turtle): the turtle
        fitnessArea (int): the number of the current food zone
    """
        #Create the circumference
    turt.speed(0)
    pi = math.pi
    turtle.colormode(255)
    turt.pos()
    print(str(turt.pos()))
    turt.write("Circle")
    turt.circle(50)

    #Draw the nest area
    turt.pencolor("blue")
    turt.width(2)
    turt.penup()
    x,y = anglePosition2(pi/4, rad)
    turt.goto(x,y)
    turt.setheading(45)
    turt.pendown()
    turt.forward(3)
    turt.backward(6)
    turt.penup()
    x,y = anglePosition2(-pi/4, rad)
    turt.goto(x,y)
    turt.setheading(-45)
    turt.pendown()
    turt.forward(3)
    turt.backward(6)
    turt.penup()
    x,y = anglePosition2(0, rad)
    turt.goto(x,y)
    turt.write("Nest")
    turt.pencolor("black")
    
    # turt.goto((rad*math.cos(0),rad+rad*math.sin(0)))

    turt.penup()

    #region draw the food spots
    for i in range(5):
        # x, y = anglePosition2(pi/2+i*pi/4, rad)
        # #Deliminate areas
        # turt.goto(x, y)
        # turt.setheading(90+i*45)
        # turt.pendown()
        # turt.width(2)
        # # turt.color(41,41,253)
        # r, g, b = random.randint(0,255),random.randint(0,255),random.randint(0,255)
        # turt.pencolor(r,g,b)
        if i == fitnessZone:
            x, y = anglePosition2(pi/2+i*pi/4, rad)
            #Deliminate areas
            turt.goto(x, y)
            turt.setheading(90+i*45)
            turt.pendown()
            # turt.color(41,41,253)
            r, g, b = random.randint(0,255),random.randint(0,255),random.randint(0,255)
            turt.pencolor(r,g,b)
            turt.pencolor("blue")
            turt.width(5)
            turt.forward(7)
            turt.write("Food Area")
        # else: 
        #     turt.forward(5)
        #     turt.write("site "+str(i+1))
        turt.penup()
    turt.pencolor(0,0,0) 
    #endregion

    #Draw the area limits
    for i in range(6):
        # x, y = anglePosition2(pi/2-pi/8+i*(pi/4), rad)
        # turt.goto(x, y)
        # turt.setheading(62.5+i*45)
        # turt.pendown()
        # turt.width(2)
        if i == fitnessZone or i-1 == fitnessZone: 
            turt.pencolor("red")
            x, y = anglePosition2(pi/2-pi/8+i*(pi/4), rad)
            turt.goto(x, y)
            turt.setheading(62.5+i*45)
            turt.pendown()
            turt.width(2)
            turt.forward(5)
            turt.backward(10)
            turt.pencolor("black")
            turt.penup()    
    turt.width(0)
    turt.hideturtle()

def isOnFood(agent, foodPos):
    """Args: agent (angle in radians)
    Returns: bool"""
    if foodPos == math.pi:
        return agent <= -math.pi+foodSize/2 or agent >= math.pi - foodSize/2

    ang1 = foodPos-foodSize/2 #     113    180-22.5 = 158  
    ang2 = foodPos+foodSize/2 #     157    180+22.5 = 202
    angMin = clampRadian(ang1)
    angMax = clampRadian(ang2)
    if angMin > angMax: #170 -+ 20 -> clamp = 150, -170, and if #-170 = 170, -190
        return agent >= angMin or agent <= angMax
        # if agent < 0: return agent <= angMax
        # else: return agent >= angMin
    # print("Angle min, max, agent: "+str(angleMin)+ " "+str(angleMax)+" "+str(agent))
    return (agent >= angMin and agent <= angMax)

def clampRadian(angle):
    """Returns a clamped radian value from [-pi, pi]
    """
    if angle > math.pi:
        return angle - 2*math.pi
    elif angle < - math.pi:
        return angle + 2*math.pi
    return angle

# def isWithin(angle, a, b):


def isOnNest(agent):
    """Args: agent (angle in rads)
    Returns: bool"""
    return agent >= -math.pi/4 and agent <= math.pi/4

def eval_genome_5Inputs(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    pi = math.pi
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitness = 0.0
    fitnesses = []

    if forcedVerbose:
        turt = turtle.Turtle()
        pen = turtle.Turtle()
    if forcedVerbose:
        #region createVisualTurtles
        # turt.clear()
        turtleRec = turtle.Turtle()
        turtleRec.fillcolor("green")
        turtleRec.shape("circle")
        turtleRec.shapesize(0.4, 0.4)
        turtleRec.penup()
        turtleRec.speed(0)
        #endregion

        #region Draw the nest area
        turt.pencolor("blue")
        turt.width(2)
        turt.penup()
        x,y = anglePosition2(pi/4, CircleRadius)
        turt.goto(x,y)
        turt.setheading(45)
        turt.pendown()
        turt.forward(3)
        turt.backward(6)
        turt.penup()
        x,y = anglePosition2(-pi/4, CircleRadius)
        turt.goto(x,y)
        turt.setheading(-45)
        turt.pendown()
        turt.forward(3)
        turt.backward(6)
        turt.penup()
        x,y = anglePosition2(0, CircleRadius)
        turt.goto(x,y)
        turt.write("Nest")
        turt.pencolor("black")

        #Create the circumference
        turt.goto(0,0)
        turt.setheading(0)
        turt.pendown()
        turt.speed(0)
        turt.pensize(0)
        pi = math.pi
        turtle.colormode(255)
        turt.pos()
        # print(str(turt.pos()))
        turt.write("Circle")
        turt.circle(50)

        # turt.goto((rad*math.cos(0),rad+rad*math.sin(0)))
        
        turt.penup()
        #endregion

    FoodAreaIds = random.sample(range(5), 3) #The id values of the food areas, 3 non repeating areas
    for run in range(RunsPerTrial):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset(); 
        counter = 0; receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        # found_food_memory = 0
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        freeze = False; prev_freeze = 0
        # curFoodAreaId = random.randint(0, 4)
        curFoodAreaId = FoodAreaIds[run]
        curFoodPos = foodPoss[curFoodAreaId]

        # verbose = Verbose and (curGen % 3 == 0) and genome_id == 500
        if forcedVerbose:
        #region newest add
            #region draw the food spots
            for i in range(5):
                if i == curFoodAreaId:
                    x, y = anglePosition2(pi/2+i*pi/4, CircleRadius)
                    #Deliminate areas
                    turt.goto(x, y)
                    turt.setheading(90+i*45)
                    turt.pendown()
                    # turt.color(41,41,253)
                    r, g, b = random.randint(0,255),random.randint(0,255),random.randint(0,255)
                    turt.pencolor(r,g,b)
                    turt.pencolor("blue")
                    turt.width(5)
                    turt.forward(7)
                    turt.write("Food Area")
                # else: 
                #     turt.forward(5)
                #     turt.write("site "+str(i+1))
                turt.penup()
            turt.pencolor(0,0,0)

            # turt.clear()
            turtleRec.clear() 
            #endregion
            #endregion

        for step in range(TimeLimit):
            if forcedVerbose and job_id == 30: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos)))
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
                input_signal = memorized_signal
            
            if not food_sensor_active:
                actions = net.activate([recCos, recSin, isOnNest(receiver), input_signal])
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            # if not freeze:
            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.activate([recCos, recSin, isOnNest(receiver), input_signal])
                        memorized_signal = actions[2]
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.activate([recCos, recSin, isOnNest(receiver), input_signal])
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.activate([recCos, recSin, isOnNest(receiver), input_signal])
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1
                if(forcedVerbose): #Change turtle graphic positions
                    if prev_food_sensor != food_sensor or prev_input_signal != input_signal or prev_found_food_bool != found_food_bool or prev_freeze != freeze or (forcedVerbose and step >= TimeLimit-1 and step >= TimeLimit-1):
                        pen.clear()
                        if(forcedVerbose and step >= TimeLimit-1 and run >=2):
                            pen.clear()
                            pen.goto(60, 50)
                            pen.write("Name = "+str(optName))    
                            pen.goto(60, 40)
                            pen.write("fitness (calculated before) = "+str(prevFitness))
                            pen.goto(60, 30)
                            pen.write("fitness = "+str(min(fitnesses)))                       

                        pen.goto(60, -10)
                        pen.write("food_sensor = "+str(food_sensor))
                        pen.goto(60, 0)
                        pen.write("input_signal = "+str(input_signal))
                        pen.goto(60, 10)
                        pen.write("found_food_bool = "+str(found_food_bool))
                        pen.goto(60, 20)
                        pen.write("freeze = "+str(freeze))
                    
                    pos = anglePosition2(receiver, CircleRadius)
                    turtleRec.goto(pos)
                
            prev_food_sensor = food_sensor
            prev_found_food_bool = found_food_bool
            prev_input_signal = input_signal
            prev_freeze = freeze
        
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeFitness)
    if forcedVerbose:
        turtle.exitonclick()
    return min(fitnesses)

def eval_genome_noComm_Viz(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # Your evaluation logic
    fitnesses = []
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    foodIds = [0,1,2,3,4]
    # random.shuffle(foodPositions)
    # random.shuffle(foodIds)
    foodIds =[random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4)]
    verbose = (Verbose and curGen % genVerb == 0 and genome_id == 300) or forcedVerbose

    FoodAreaIds = random.sample(range(5), 3) #The id values of the food areas, 3 non repeating areas
    for run in range(RunsPerTrial):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset(); 
        counter = 0; prevCounter = 0 
        receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        curFoodPos = foodPoss[foodIds[run]]

        if verbose:
            agentVisuals.reset_environment()
            agentVisuals.draw_food_spot(foodIds[run])
        for step in range(TimeLimit):
            if  curGen % genVerb == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos))+" pos = "+str(receiver/math.pi*180)+ " FoodPos="+str(curFoodPos/math.pi*180)+ " Counter = "+str(counter))
 
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
            
            if not food_sensor_active:
                actions = net.activate([recCos, recSin, isOnNest(receiver)])
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            # if not freeze:
            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.activate([recCos, recSin, isOnNest(receiver)])
                        # input_signal = actions[2]
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.activate([recCos, recSin, isOnNest(receiver)])
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.activate([recCos, recSin, isOnNest(receiver)])
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            if verbose:
                agentVisuals.move_agent(receiver)
            if verbose and (prev_food_sensor != food_sensor or prev_found_food_bool != found_food_bool or prev_input_signal != input_signal or prevCounter != counter):
                prev_food_sensor = food_sensor; prev_found_food_bool = found_food_bool; prev_input_signal = input_signal; prevCounter = counter
                s = 0
                for f in fitnesses: s += f
                res = s/len(fitnesses) if len(fitnesses) > 0 else s
                sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "counter = "+str(counter), "pos = "+str(receiver/math.pi*180), "foodArea = ["+str(curFoodPos-foodSize/2)+" "+str(curFoodPos+foodSize/2)+"]", "returnedToNest = "+str(returnedToNest), "average score = "+str(res)]
                agentVisuals.write(sentenceList)


            #Evaluate score (in last steps)
            if returnedToNest and step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1
        fitnesses.append(counter/TimeFitness)
    s = 0
    for f in fitnesses:
        s+=f
    res = s/len(fitnesses)
    if verbose:
        sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "counter = "+str(counter), "pos = "+str(receiver/math.pi*180), "foodArea = ["+str(curFoodPos-foodSize/2)+" "+str(curFoodPos+foodSize/2)+"]", "returnedToNest = "+str(returnedToNest), "average score = "+str(res)]
        agentVisuals.write(sentenceList)
    return res

def eval_genome_noComm_2(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    pi = math.pi
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitness = 0.0
    fitnesses = []

    # FoodAreaIds = random.sample(range(5), 3) #The id values of the food areas, 3 non repeating areas
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    random.shuffle(foodPositions)

    for run in range(len(foodPositions)):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset(); 
        counter = 0; receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        # found_food_memory = 0
        # input_signal = 0; prev_input_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        freeze = False; prev_freeze = 0
        # curFoodAreaId = random.randint(0, 4)
        curFoodPos = foodPositions[run]

        for step in range(TimeLimit):
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
            
            # if not food_sensor_active:
            actions = net.activate([recCos, recSin, isOnNest(receiver)])
            recAct = (actions[0], actions[1])
            receiver = one_step(receiver, recAct)

            # # if not freeze:
            # if food_sensor_active:
            #     if isOnFood(receiver, curFoodPos):
            #         food_sensor = 1
            #         if not found_food_bool:
            #             actions = net.activate([recCos, recSin, isOnNest(receiver)])
            #             # input_signal = actions[2]
            #             recAct = (actions[0], actions[1])
            #             receiver = one_step(receiver, recAct)
            #             found_food_bool = True
            #         if found_food_bool:
            #             actions = net.activate([recCos, recSin, isOnNest(receiver)])
            #             recAct = (actions[0], actions[1])
            #             receiver = one_step(receiver, recAct)    
            #     elif not isOnFood(receiver, curFoodPos):
            #         food_sensor = 0
            #         actions = net.activate([recCos, recSin, isOnNest(receiver)])
            #         recAct = (actions[0], actions[1])
            #         receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1
                
            prev_food_sensor = food_sensor
            prev_found_food_bool = found_food_bool
            # prev_input_signal = input_signal
            prev_freeze = freeze
        
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeLimit)
    if forcedVerbose:
        turtle.exitonclick()
    return sum(fitnesses)

def eval_genome_noComm_CTRNN(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    pi = math.pi
    advance_time = 1
    time_step = 0.5
    net = neat.ctrnn.CTRNN.create(genome, config, time_step)
    # neat.ctrnn.CTRNN.create()
    fitness = 0.0
    fitnesses = []

    # FoodAreaIds = random.sample(range(5), 3) #The id values of the food areas, 3 non repeating areas
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    random.shuffle(foodPositions)

    for run in range(len(foodPositions)):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset(); 

        counter = 0; receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        # found_food_memory = 0
        # input_signal = 0; prev_input_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        freeze = False; prev_freeze = 0
        # curFoodAreaId = random.randint(0, 4)
        curFoodPos = foodPositions[run]

        for step in range(TimeLimit):
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
            
            # if not food_sensor_active:
            actions = net.advance([recCos, recSin, isOnNest(receiver)], advance_time, time_step)
            recAct = (actions[0], actions[1])
            receiver = one_step(receiver, recAct)

            # # if not freeze:
            # if food_sensor_active:
            #     if isOnFood(receiver, curFoodPos):
            #         food_sensor = 1
            #         if not found_food_bool:
            #             actions = net.activate([recCos, recSin, isOnNest(receiver)])
            #             # input_signal = actions[2]
            #             recAct = (actions[0], actions[1])
            #             receiver = one_step(receiver, recAct)
            #             found_food_bool = True
            #         if found_food_bool:
            #             actions = net.activate([recCos, recSin, isOnNest(receiver)])
            #             recAct = (actions[0], actions[1])
            #             receiver = one_step(receiver, recAct)    
            #     elif not isOnFood(receiver, curFoodPos):
            #         food_sensor = 0
            #         actions = net.activate([recCos, recSin, isOnNest(receiver)])
            #         recAct = (actions[0], actions[1])
            #         receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1
                
            prev_food_sensor = food_sensor
            prev_found_food_bool = found_food_bool
            # prev_input_signal = input_signal
            prev_freeze = freeze
        
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeLimit)
    if forcedVerbose:
        turtle.exitonclick()
    return sum(fitnesses)

def eval_genome3(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    pi = math.pi
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    fitness = 0.0
    # Your evaluation logic
    fitnesses = []
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    # random.shuffle(foodPositions)
    foodPositions = [foodPositions[random.randint(0,4)], foodPositions[random.randint(0,4)], foodPositions[random.randint(0,4)], foodPositions[random.randint(0,4)], foodPositions[random.randint(0,4)]]

    for run in range(len(foodPositions)):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset(); 
        counter = 0; receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        freeze = False; prev_freeze = 0
        curFoodAreaId = random.randint(0, 4)
        curFoodPos = foodPositions[run]


        for step in range(TimeLimit):
            # print("genome_id " +str(genome_id))
            if  curGen % genVerb == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos))+" pos = "+str(receiver/math.pi*180)+ " FoodPos="+str(curFoodPos/math.pi*180)+ " Counter = "+str(counter))
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
                input_signal = memorized_signal
            
            if not food_sensor_active:
                actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            # if not freeze:
            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                        memorized_signal = actions[2]
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if step >= TimeLimit-TimeFitness:#TimeFitness:
                if returnedToNest and isOnFood(receiver, curFoodPos): 
                    counter+=1
                
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeFitness)
    sum = 0
    for f in fitnesses:
        sum += f
    res = sum/len(fitnesses)
    return res

def eval_genome3CTRNN(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    pi = math.pi
    net = neat.ctrnn.CTRNN.create(genome, config, 1)
    fitness = 0.0
    # Your evaluation logic
    fitnesses = []
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    random.shuffle(foodPositions)
    foodPositions = foodPositions[0], foodPositions[1], foodPositions[2]

    for run in range(RunsPerTrial):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        net.reset(); 
        counter = 0; receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        freeze = False; prev_freeze = 0
        curFoodAreaId = random.randint(0, 4)
        curFoodPos = foodPositions[run]


        for step in range(TimeLimit):
            # print("genome_id " +str(genome_id))
            if  curGen % 10 == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos))+" pos = "+str(receiver/math.pi*180)+ " FoodPos="+str(curFoodPos/math.pi*180))
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
                input_signal = memorized_signal
            
            if not food_sensor_active:
                actions = net.advance([recCos, recSin, isOnNest(receiver), input_signal], 1, 0.2)
                # actions = net.activate([recCos, recSin, isOnNest(receiver), input_signal])
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            # if not freeze:
            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.advance([recCos, recSin, isOnNest(receiver), input_signal], 1, 0.2)
                        # actions = net.activate([recCos, recSin, isOnNest(receiver), input_signal])
                        memorized_signal = actions[2]
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.advance([recCos, recSin, isOnNest(receiver), input_signal], 1, 0.2)
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.advance([recCos, recSin, isOnNest(receiver), input_signal], 1, 0.2)
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1
                
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeFitness)
    sum = 0
    for f in fitnesses:
        sum += f
    res = sum/len(fitnesses)
    return (res)


def eval_genomeNoComm_Viz(genome, config, curGen=-1, genome_id=-1, forcedVerbose=False, makeGif=False, gifPath=None, curRun=-1):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # Your evaluation logic
    fitnesses = []
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    foodIds = [0,1,2,3,4]
    # random.shuffle(foodPositions)
    random.shuffle(foodIds)
    # foodIds =[random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4)]
    verbose = (Verbose and curGen % genVerb == 0 and genome_id == 150) or forcedVerbose

    for run in range(len(foodIds)):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset()
        #prev values are only for updating verbose/visual differences
        counter = 0; prevCounter = 0 
        receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        curFoodPos = foodPoss[foodIds[run]]

        if verbose:
            agentVisuals.reset_environment()
            agentVisuals.draw_food_spot(foodIds[run])
        for step in range(TimeLimit):
            # if  curGen % genVerb == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos))+" pos = "+str(receiver/math.pi*180)+ " FoodPos="+str(curFoodPos/math.pi*180)+ " Counter = "+str(counter))
            # print("genome_id " +str(genome_id))
            # if  curGen % 10 == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos)))
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                food_sensor_active = False
                input_signal = memorized_signal
            
            if not food_sensor_active:
                actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                        memorized_signal = 0
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if returnedToNest and step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1

            if verbose:
                agentVisuals.move_agent(receiver)
                if (prev_food_sensor != food_sensor or prev_found_food_bool != found_food_bool or prev_input_signal != input_signal or prevCounter != counter):
                    prev_food_sensor = food_sensor; prev_found_food_bool = found_food_bool; prev_input_signal = input_signal; prevCounter = counter
                    s = 0
                    for f in fitnesses: s += f
                    res = s/len(fitnesses) if len(fitnesses) > 0 else s
                    sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "counter = "+str(counter), "pos = "+str(receiver/math.pi*180), "foodArea = ["+str(curFoodPos-foodSize/2)+" "+str(curFoodPos+foodSize/2)+"]", "returnedToNest = "+str(returnedToNest), "average score = "+str(res)]
                    agentVisuals.write(sentenceList)
                num = int((step+run*TimeLimit)/gifGranularity)
                frameNum = orderNum(num)
                # print("frameNum "+str(frameNum))
                # print("Remainding 0s "+str(remaindingZeros))
                if makeGif and (step%gifGranularity==0 or step>=99): save_layout("".join([gifPath,"/eval_genomeNoComm_Viz/run",str(curRun),"/frames/"]), "".join([frameNum,".jpeg"]))

                
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeFitness)
    s = 0
    for f in fitnesses:
        s+=f
    res = s/len(fitnesses)
    if verbose:
        sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "counter = "+str(counter), "pos = "+str(receiver/math.pi*180), "foodArea = ["+str(curFoodPos-foodSize/2)+" "+str(curFoodPos+foodSize/2)+"]", "returnedToNest = "+str(returnedToNest), "average score = "+str(res)]
        agentVisuals.write(sentenceList)
    if makeGif:
        # print("".join([gifPath,"/eval_genomeNoComm_Viz/run",str(curRun)]))
        # print("".join([gifPath,"/eval_genomeNoComm_Viz/run",str(curRun),"GIF"]))
        num = int((step+run*TimeLimit)/gifGranularity)
        frameNum = orderNum(num+1)
        if makeGif and (step%gifGranularity==0 or step>=99): save_layout("".join([gifPath,"/eval_genomeNoComm_Viz/run",str(curRun),"/frames/"]), "".join([frameNum,".jpeg"]))
        make_gif("".join([gifPath,"/eval_genomeNoComm_Viz/run",str(curRun),"/frames/"]),"".join([gifPath,"/eval_genomeNoComm_Viz/run",str(curRun),"/run",str(curRun),"_Score",str(res),"_","GIF.gif"]))
    return res

def eval_genome3_Viz(genome, config, curGen=-1, genome_id=-1, forcedVerbose=False, makeGif=False, gifPath=None, curRun=-1):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    # Your evaluation logic
    fitnesses = []
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    foodIds = [0,1,2,3,4]
    # random.shuffle(foodPositions)
    random.shuffle(foodIds)
    # foodIds =[random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4)]
    verbose = (Verbose and curGen % genVerb == 0 and genome_id == 150) or forcedVerbose

    for run in range(len(foodIds)):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        # net.reset()
        #prev values are only for updating verbose/visual differences
        counter = 0; prevCounter = 0 
        receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        curFoodPos = foodPoss[foodIds[run]]

        if verbose:
            agentVisuals.reset_environment()
            agentVisuals.draw_food_spot(foodIds[run])
        for step in range(TimeLimit):
            # if  curGen % genVerb == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos))+" pos = "+str(receiver/math.pi*180)+ " FoodPos="+str(curFoodPos/math.pi*180)+ " Counter = "+str(counter))
            # print("genome_id " +str(genome_id))
            # if  curGen % 10 == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos)))
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                food_sensor_active = False
                input_signal = memorized_signal
            
            if not food_sensor_active:
                actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                        memorized_signal = actions[2]
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.activate([recCos, recSin, food_sensor, input_signal, returnedToNest])
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            #Evaluate score (in last steps)
            if returnedToNest and step >= TimeLimit-TimeFitness:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1

            if verbose:
                agentVisuals.move_agent(receiver)
                if (prev_food_sensor != food_sensor or prev_found_food_bool != found_food_bool or prev_input_signal != input_signal or prevCounter != counter):
                    prev_food_sensor = food_sensor; prev_found_food_bool = found_food_bool; prev_input_signal = input_signal; prevCounter = counter
                    s = 0
                    for f in fitnesses: s += f
                    res = s/len(fitnesses) if len(fitnesses) > 0 else s
                    sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "counter = "+str(counter), "pos = "+str(receiver/math.pi*180), "foodArea = ["+str(curFoodPos-foodSize/2)+" "+str(curFoodPos+foodSize/2)+"]", "returnedToNest = "+str(returnedToNest), "average score = "+str(res)]
                    agentVisuals.write(sentenceList)
                num = int((step+run*TimeLimit)/gifGranularity)
                frameNum = orderNum(num)
                remaindingZeros = 3 - len(frameNum)
                for i in range(remaindingZeros):
                    frameNum = "".join(["0",frameNum])
                # print("frameNum "+str(frameNum))
                # print("Remainding 0s "+str(remaindingZeros))
                if makeGif and (step%gifGranularity==0 or step>=99): save_layout("".join([gifPath,"/eval_genome3_Viz/run",str(curRun),"/frames/"]), "".join([frameNum,".jpeg"]))

                
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeFitness)
    s = 0
    for f in fitnesses:
        s+=f
    res = s/len(fitnesses)
    if verbose:
        sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "counter = "+str(counter), "pos = "+str(receiver/math.pi*180), "foodArea = ["+str(curFoodPos-foodSize/2)+" "+str(curFoodPos+foodSize/2)+"]", "returnedToNest = "+str(returnedToNest), "average score = "+str(res)]
        agentVisuals.write(sentenceList)
    if makeGif:
        # print("".join([gifPath,"/eval_genome3_Viz/run",str(curRun)]))
        # print("".join([gifPath,"/eval_genome3_Viz/run",str(curRun),"GIF"]))
        num = int((step+run*TimeLimit)/gifGranularity)
        frameNum = orderNum(num+1)
        save_layout("".join([gifPath,"/eval_genome3_Viz/run",str(curRun),"/frames/"]), "".join([frameNum,".jpeg"]))
        make_gif("".join([gifPath,"/eval_genome3_Viz/run",str(curRun),"/frames/"]),"".join([gifPath,"/eval_genome3_Viz/run",str(curRun),"/run",str(curRun),"_Score",str(res),"_","GIF.gif"]))
    return res

def eval_genome3CTRNN_Viz(genome, config, curGen=-1, genome_id=-1, job_id=-1, core_id=-1, forcedVerbose=False, optName = "", prevFitness = -1):
    pi = math.pi
    time_const = 1
    adv_time = 1
    time_step = 0.1
    net = neat.ctrnn.CTRNN.create(genome, config, time_const)
    fitness = 0.0
    # Your evaluation logic
    fitnesses = []
    foodPositions = [math.pi/2, 3*math.pi/4, math.pi, -3*math.pi/4, -math.pi/2]
    foodIds = [0,1,2,3,4]
    # random.shuffle(foodPositions)
    # random.shuffle(foodIds)
    foodIds =[random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4), random.randint(0,4)]
    verbose = (Verbose and curGen %50 == 0 and genome_id == 300) or forcedVerbose

    for run in range(len(foodIds)):
        #When the simulation starts, the food-sensor signal is 0, 
        #and when the agent is out of the nest, it will become 1
        #if the agent is on the food spot or 0 if else. 
        #If the food-sensor is 1, an angular position of the 
        #agent is measured and fed to the ANN. Now the 
        #(time t) the ANN is fed with the position and maybe the
        #sensor value, and at time t+1 the output signal is
        #memorized as found_food_mem or something with 
        #another name. When the agent returns, the 
        #found_food_mem will be forever fed to the ANN.

        net.reset(); 
        counter = 0; receiver=0
        food_sensor = 0; prev_food_sensor = 0
        food_sensor_active = True
        found_food_bool = False; prev_found_food_bool = False
        input_signal = 0; prev_input_signal = 0
        memorized_signal = 0
        wasOutOfNest = False #Whether the agent was out of the nest in the previous step (helper variable for returnedToNest)
        returnedToNest = False #Whether the agent was out of the nest and came back
        freeze = False; prev_freeze = 0
        curFoodPos = foodPoss[foodIds[run]]

        if verbose:
            agentVisuals.reset_environment()
            agentVisuals.draw_food_spot(foodIds[run])
        for step in range(TimeLimit):
            if  curGen % genVerb == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos))+" pos = "+str(receiver/math.pi*180)+ " FoodPos="+str(curFoodPos/math.pi*180)+ " Counter = "+str(counter))
            # print("genome_id " +str(genome_id))
            # if  curGen % 10 == 0 and genome_id == 10: print("step="+str(step)+" isOnNest="+str(isOnNest(receiver))+" wasOutOfNest = "+str(wasOutOfNest)+" returnedToNest = "+str(returnedToNest)+" freeze = "+str(freeze) + " inpSignal = "+str(input_signal) +" mem_signal = "+str(memorized_signal) +" food_sensor = "+str(food_sensor)+" isOnFood = "+str(isOnFood(receiver, curFoodPos)))
            #1,2 Positions:
            # sendCos, sendSin = get_input(sender)
            recCos, recSin = get_input(receiver)

            if not isOnNest(receiver):
                wasOutOfNest = True

            if wasOutOfNest and isOnNest(receiver):
                returnedToNest = True

            if returnedToNest: #and not freeze:
                freeze = True
                food_sensor_active = False
                input_signal = memorized_signal
            
            if not food_sensor_active:
                actions = net.advance([recCos, recSin, food_sensor, input_signal], adv_time, time_step)
                recAct = (actions[0], actions[1])
                receiver = one_step(receiver, recAct)

            # if not freeze:
            if food_sensor_active:
                if isOnFood(receiver, curFoodPos):
                    food_sensor = 1
                    if not found_food_bool:
                        actions = net.advance([recCos, recSin, food_sensor, input_signal], adv_time, time_step)
                        memorized_signal = actions[2]
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)
                        found_food_bool = True
                    if found_food_bool:
                        actions = net.advance([recCos, recSin, food_sensor, input_signal], adv_time, time_step)
                        recAct = (actions[0], actions[1])
                        receiver = one_step(receiver, recAct)    
                elif not isOnFood(receiver, curFoodPos):
                    food_sensor = 0
                    actions = net.advance([recCos, recSin, food_sensor, input_signal], adv_time, time_step)
                    recAct = (actions[0], actions[1])
                    receiver = one_step(receiver, recAct)

            if verbose:
                agentVisuals.move_agent(receiver)
            if verbose and (prev_food_sensor != food_sensor or prev_found_food_bool != found_food_bool or prev_input_signal != input_signal):
                prev_food_sensor = food_sensor; prev_found_food_bool = found_food_bool; prev_input_signal = input_signal
                sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal) ]
                agentVisuals.write(sentenceList)

            #Evaluate score (in last steps)
            if step >= TimeLimit-TimeFitness and returnedToNest:#TimeFitness:
                if isOnFood(receiver, curFoodPos): 
                    counter+=1
                
        # fitnesses.append(counter/TimeFitness)
        fitnesses.append(counter/TimeFitness)
    sum = 0
    for f in fitnesses:
        sum+=f
    res = sum/len(fitnesses)
    if verbose:
        sentenceList =["food_sensor = "+str(food_sensor), "found_food_bool = "+str(found_food_bool), "input_signal = "+str(input_signal), "average fitness = "+ str(res) + " Counter = "+str(counter)]
        agentVisuals.write(sentenceList)
    return res


def eval_genomes(genomes, config, gen, run, evalGenomeFunc):
    """
    The function to evaluate the fitness of each genome in 
    the genomes list. 
    The provided configuration is used to create continuous-time 
    recurrent neural network from each genome and after that created
    the neural network evaluated in its ability to solve
    sender-bee problem. .
    Arguments:
        genomes: The list of genomes from population in the 
                current generation
        config: The configuration settings with algorithm
                hyper-parameters
    """
    # genome_id = 0
    verbose = False
    prevGen = gen
    genome_count = 0
    for genome_id, genome in genomes:
        #print("\nGENOME COUNT", genome_count )
        # if gen >= NUM_GENERATIONS-1:
        #     verbose = True
        #     print("Verbose is True")
        #     genome.fitness = eval_genome2(genome, config, forcedVerbose=True)
        #     break
        # print("Verbose is False")
        genome.fitness = evalGenomeFunc(genome,config,curGen=gen,curRun=run,genome_id=genome_count,forcedVerbose=False)#, forcedVerbose=False)
        genome_count = genome_count+1


def run_single():
    local_dir = os.getcwd()
    config_path = os.path.join(local_dir, 'config-singleBeeComANN.ini')
    # config_path = os.path.join(local_dir, 'config-singleBeeComANN_NoComm.ini')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    pop = PopulationMod.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    # evalFunc = eval_genome3_Viz
    agentVisuals.turt.speed(0) 
    # evalFunc = eval_genomeNoComm_Viz
    evalFunc = eval_genome3_Viz
    # evalFunc = eval_genome_noComm_2
    winner=pop.run2(eval_genomes,evalFunc,NUM_GENERATIONS)
    di_best=pop.reporters.reporters[0].best_genome()
    fit = evalFunc(winner, config, forcedVerbose=False)
    print("fitness of (re evaluated) "+str(evalFunc.__name__)+" is "+str(fit))
    turtle.speed(0)
    # eval_genome3_Viz(winner, config, forcedVerbose=True)
    evalFunc(winner, config, forcedVerbose=True, makeGif=True, gifPath="gifs")

    print("visualize.__file__ = ",visualize.__file__)
    visualize.plot_stats(stats, ylog=True, view=True, filename="ann-fitness.svg")
    visualize.plot_species(stats, view=True, filename="ann-speciation.svg")
    # visualize.plt()

    node_names = {-1: 'cos', -2: 'sin', -3: 'nest', -4: 'signal', \
                  0: 'speedL', 1: 'speedR', 2: 'signal'}
    visualize.draw_net(config, di_best, True, node_names=node_names)

    visualize.draw_net(config, di_best, view=True, node_names=node_names,
                       filename="di_best-ann.gv")

    # Save the winner.
    with open('di_best-ann', 'wb') as f:
        pickle.dump(di_best, f)
    with open('winner-ann', 'wb') as f:
        pickle.dump(winner, f)
    #Visualize winner
    # eval_genome3_Viz(di_best, config, forcedVerbose=True)
    # eval_genome_5Inputs(winner, config, forcedVerbose=True)
    # eval_genome_noComm(winner, config, forcedVerbose=True)
    return fit


def run2():
    # NUM_GENERATIONS=1000
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    #local_dir = os.path.dirname(__file__)
    local_dir = os.getcwd()
    config_path = os.path.join(local_dir, 'config-singleBeeComANN.ini')
    config_path2 = os.path.join(local_dir, 'config-singleBeeComANN_NoComm.ini')
    # config_path = os.path.join('config-Rec_ctrnn.ini')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    config2 = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path2)
    configPaths = [config_path, config_path2]
    # configPaths = [config_path]

    # configPaths = [config_path]# Just comm
    evalFuncs = [eval_genome3_Viz, eval_genomeNoComm_Viz]
    visFuncs = [eval_genome3_Viz, eval_genomeNoComm_Viz]
    # evalFuncs = [eval_genome3_Viz]
    # visFuncs = [eval_genome3_Viz]

    fitnesses = dict()
    for func in evalFuncs:
        fitnesses.update({func.__name__:[]})
    
    reps = 20
    for r in range(reps):
        try:
            for i in range(len(evalFuncs)):
                config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 configPaths[i])
                evalFunc = evalFuncs[i]
                pop = PopulationMod.Population(config)
                stats = neat.StatisticsReporter()
                pop.add_reporter(stats)
                pop.add_reporter(neat.StdOutReporter(True))

                #pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
                # winner = pop.run(pe.evaluate)
                winner=pop.run2(eval_genomes,evalFunc,NUM_GENERATIONS)
                di_best=pop.reporters.reporters[0].best_genome()
                # Save the winner.
                with open('di_best-ann', 'wb') as f:
                    pickle.dump(di_best, f)

                # print('Winner:',winner)
                # print('DI best:',di_best)
                print("lastGenomeWinner fitness (retest) = ", winner.fitness)
                evalFunc(winner, config, forcedVerbose=False)
                # print("All time winner fitness (retest) = ", di_best.fitness)
                # eval_genome2(di_best, config, forcedVerbose=True, optName="All time winner", prevFitness=di_best.fitness)

                #eval_genome(winner,config)
                fitnessGen = stats.get_fitness_mean()[-1]
                print(fitnesses)
                print(evalFunc.__name__)
                fitnesses[evalFunc.__name__].append(fitnessGen)

                strRep = orderNum(r)
                print("visualize.__file__ = ",visualize.__file__)
                folderFit = "".join(["stats/run",strRep,"/gen_fitness_stats/",str(evalFunc.__name__),"/"])
                if not os.path.exists(folderFit):  os.makedirs(folderFit)
                folderANN = "".join(["stats/run",strRep,"/ann_speciation/",str(evalFunc.__name__),"/"])
                if not os.path.exists(folderANN):  os.makedirs(folderANN)
                visualize.plot_stats(stats, ylog=True, view=False, filename="".join([folderFit,"run",strRep,"_ann-fitness.svg"]))
                visualize.plot_species(stats, view=False, filename="".join([folderANN,"run",strRep,"_ann-speciation.svg"]))
                node_names = {-1: 'cos', -2: 'sin', -3: 'nest', -4: 'signal', \
                    0: 'speedL', 1: 'speedR', 2: 'signal'}
                folderANNstructure = "".join(["stats/run",strRep,"/ann_structures/",str(evalFunc.__name__),"/"])
                if not os.path.exists(folderANNstructure):  os.makedirs(folderANNstructure)
                visualize.draw_net(config, di_best, view=False, node_names=node_names,
                           filename="".join(["stats/run",strRep,"/ann_structures/",str(evalFunc.__name__),"/run",strRep,"DI_best.gv"]))
                with open('di_best-ann', 'wb') as f:
                    pickle.dump(di_best, f)

            # print("fitness of "+str(visFuncs[i].__name__)+" (vis) = "+str(visFuncs[i](winner,config, forcedVerbose=False)))
                print("fitness of "+str(visFuncs[i].__name__)+" (vis) = "+str(    evalFunc(winner, config, forcedVerbose=True, makeGif=True, gifPath="gifs", curRun=r)))

        except:
            print("Exception occurred, skipping rep")
            print("last fitnesses of each evalFunc: ")
            print(fitnesses)
            continue
        print("last fitnesses of each evalFunc: ")
        print(fitnesses)

    # for i in range(len(visFuncs)):
    #     config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
    #             neat.DefaultSpeciesSet, neat.DefaultStagnation,
    #             configPaths[i])
    #     evalFunc = visFuncs[i]
    #     pop = PopulationMod.Population(config)
    #     print("fitness of "+str(visFuncs[i].__name__)+" = "+str(evalFunc()))


    print("last fitnesses of each evalFunc: ")
    print(fitnesses)
    print("last fitnesses of each evalFunc/reps: ")
    # for k in fitnesses:
    #     print(str(k)+" fitnesses = "+str(fitnesses[k]/reps))
    print("last average fitnesses of each evalFunc")
    for k in fitnesses:
        print(str(k)+" average fitness = "+str(sum(fitnesses[k])/len(fitnesses[k])))

def extractDictValues(dl):
    return

def saveImg():
    import tkinter # Python 3
    ts = agentVisuals.turt.getscreen()
    # turtle.forward(100)
    # ts = turtle.getscreen()

    ts.getcanvas().postscript(file="duck.eps")

def save_layout(folder=None, filename="gifs/duck.jpeg"):
    ps = turtle.getscreen().getcanvas().postscript(colormode="color")
    im = Image.open(io.BytesIO(ps.encode("utf-8")))
    if folder is not None:
        if not os.path.exists(folder):
            os.makedirs(folder)
    f = os.path.join(folder, filename)
    im.save(f, format="jpeg")

def make_gif(frame_folder, save_path):
    frames = [Image.open(image) for image in glob.glob("".join([frame_folder,"*.JPEG"]))]
    frame_one = frames[0]
    frame_one.save(save_path, format="GIF", append_images=frames,
               save_all=True, duration=10, loop=1)

def runPrevBest(option, makeGif=False):
    if option==0: file = "/di_best-ann" 
    elif option==1: file = "/winner-ann"
    local_dir = os.getcwd()
    config_path = os.path.join(local_dir, 'config-singleBeeComANN.ini')
    # config_path = os.path.join(local_dir, 'config-singleBeeComANN_NoComm.ini')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    with open(local_dir+"/di_best-ann", "rb") as f:
        genome = pickle.load(f)

    agentVisuals.turt.speed(0) 
    eval_genome3_Viz(genome, config, forcedVerbose=True, makeGif=makeGif, gifPath="gifs", curRun=-10)


if __name__ == '__main__':
    radius = 50 #Only important if Verbose
    agentVisuals.reset_environment()
    agentVisuals.draw_food_spot(2)

    # run_single()
    # run2()
    # runPrevBest(0, True)
    # debug()
    # saveImg()
    # save_layout()
    # make_gif("gifs/eval_genome3_Viz/run-10/")
    Verbose=True
    if Verbose:
        turtle.exitonclick()


#region Maybe use these functions below later

# def run_experimentCopy(config_file):
#     """
#     The function to run XOR experiment against hyper-parameters
#     defined in the provided configuration file.
#     The winner genome will be rendered as a graph as well as the
#     important statistics of neuroevolution process execution.
#     Arguments:
#         config_file: the path to the file with experiment
#                     configuration
#     """
#     # Load configuration.
#     config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_file)

#     # Create the population, which is the top-level object for a NEAT run.
#     p = neat.Population(config)

#     # Add a stdout reporter to show progress in the terminal.
#     p.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     p.add_reporter(stats)
#     p.add_reporter(neat.Checkpointer(5, filename_prefix='out/neat-checkpoint-'))

#     # Run for up to 300 generations.
#     best_genome = p.run(eval_genomes, 3)

#     # Display the best genome among generations.
#     print('\nBest genome:\n{!s}'.format(best_genome))

# def clean_output():
#     if os.path.isdir(out_dir):
#         # remove files from previous run
#         shutil.rmtree(out_dir)

#     # create the output directory
#     os.makedirs(out_dir, exist_ok=False)

# if __name__ == '__main__':
#     # Determine path to configuration file. This path manipulation is
#     # here so that the script will run successfully regardless of the
#     # current working directory.
#     config_path = os.path.join(local_dir, 'xor_config.ini')

#     # Clean results of previous run if any or init the ouput directory
#     clean_output()

#     # Run the experiment
#     run_experimentCopy(config_path)

#endregion