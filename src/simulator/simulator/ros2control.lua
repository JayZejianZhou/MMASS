function sysCall_init()
    robotHandle=sim.getObjectAssociatedWithScript(sim.handle_self)
    leftMotor=sim.getObjectHandle("ros2InterfaceControlledBubbleRobLeftMotor") -- Handle of the left motor
    rightMotor=sim.getObjectHandle("ros2InterfaceControlledBubbleRobRightMotor") -- Handle of the right motor
    noseSensor=sim.getObjectHandle("ros2InterfaceControlledBubbleRobSensingNose") -- Handle of the proximity sensor
    -- Launch the ROS2 client application:
    if simROS2 then
        sim.addLog(sim.verbosity_scriptinfos,"ROS2 interface was found.")
        local sysTime=sim.getSystemTimeInMs(-1) 
        local leftMotorTopicName='leftMotorSpeed'..sysTime -- we add a random component so that we can have several instances of this robot running
        local rightMotorTopicName='rightMotorSpeed'..sysTime -- we add a random component so that we can have several instances of this robot running
        local sensorTopicName='sensorTrigger'..sysTime -- we add a random component so that we can have several instances of this robot running
        local simulationTimeTopicName='simTime'..sysTime -- we add a random component so that we can have several instances of this robot running
        -- Prepare the sensor publisher and the motor speed subscribers:
        sensorPub=simROS2.createPublisher('/'..sensorTopicName,'std_msgs/msg/Bool')
        simTimePub=simROS2.createPublisher('/'..simulationTimeTopicName,'std_msgs/msg/Float32')
        leftMotorSub=simROS2.createSubscription('/'..leftMotorTopicName,'std_msgs/msg/Float32','setLeftMotorVelocity_cb')
        rightMotorSub=simROS2.createSubscription('/'..rightMotorTopicName,'std_msgs/msg/Float32','setRightMotorVelocity_cb')
        -- Now we start the client application:
        result=sim.launchExecutable('ros2BubbleRob',leftMotorTopicName.." "..rightMotorTopicName.." "..sensorTopicName.." "..simulationTimeTopicName,0)
    else
        sim.addLog(sim.verbosity_scripterrors,"ROS2 interface was not found. Cannot run.")
    end
    
end
function setLeftMotorVelocity_cb(msg)
    -- Left motor speed subscriber callback
    sim.setJointTargetVelocity(leftMotor,msg.data)
end

function setRightMotorVelocity_cb(msg)
    -- Right motor speed subscriber callback
    sim.setJointTargetVelocity(rightMotor,msg.data)
end

function getTransformStamped(objHandle,name,relTo,relToName)
    t=sim.getSystemTime()
    p=sim.getObjectPosition(objHandle,relTo)
    o=sim.getObjectQuaternion(objHandle,relTo)
    return {
        header={
            stamp={sec=math.floor(t),nanosec=(t-math.floor(t))*10^9},
            frame_id=relToName
        },
        child_frame_id=name,
        transform={
            translation={x=p[1],y=p[2],z=p[3]},
            rotation={x=o[1],y=o[2],z=o[3],w=o[4]}
        }
    }
end


function sysCall_actuation()
    -- Send an updated sensor and simulation time message, and send the transform of the robot:
    if simROS2 then
        local result=sim.readProximitySensor(noseSensor)
        local detectionTrigger={}
        detectionTrigger['data']=result>0
        simROS2.publish(sensorPub,detectionTrigger)
        simROS2.publish(simTimePub,{data=sim.getSimulationTime()})
        -- Send the robot's transform:
        simROS2.sendTransform(getTransformStamped(robotHandle,'ros2InterfaceControlledBubbleRob',-1,'world'))
        -- To send several transforms at once, use simROS2.sendTransforms instead
    end
end

function sysCall_cleanup()
    if simROS2 then
        -- Following not really needed in a simulation script (i.e. automatically shut down at simulation end):
        simROS2.shutdownPublisher(sensorPub)
        simROS2.shutdownSubscription(leftMotorSub)
        simROS2.shutdownSubscription(rightMotorSub)
    end
end
