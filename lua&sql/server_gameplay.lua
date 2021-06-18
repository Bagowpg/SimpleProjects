setTime(12,30)
pocketmoney = 0
function Spawn(X, Y, Z, angle, idSkin, money)
	spawnPlayer(source, X, Y, Z, angle, idSkin)
	setCameraTarget(source, source)
	setPlayerMoney(source, money, false)
end
addEvent("spawnPlayer", true ) -- необходимо для передачи на клиент
addEventHandler("spawnPlayer", getRootElement(), Spawn)
createPickup(1144, -2037, 69, 3, 1212, 10000) -- деньги горожан
createPickup(-2268, 151, 35, 3, 1212, 10000)  -- деньги пришельцев
createVehicle(412, 1155, -2028, 69, 0, 0, 90)
createVehicle(420, 1155, -2023, 69, 0, 0, 90)
createVehicle(601, 1155, -2018, 69, 0, 0, 90)
createPickup(1150, -2028, 69, 3, 1239, 10000)  -- транспорт
createPickup(1150, -2023, 69, 3, 1239, 10000)  -- транспорт
createPickup(1150, -2018, 69, 3, 1239, 10000)  -- транспорт
function pickupUse(thePlayer)
	local x,y,z = getElementPosition(source)
    if (x == 1144 and y == -2037 and z == 69) or  (x == -2268 and y == 151 and z == 35)then
		local login = getElementData(root, "login", false)
		pocketmoney = getPlayerMoney(thePlayer)
		setPlayerMoney(thePlayer, pocketmoney + 100000, false)
		triggerEvent("NewData", thePlayer, "players", "money", getPlayerMoney(thePlayer))
	elseif x == 1150 and y == -2028 and z == 69 then
		triggerClientEvent("onOffer", source, 412)
	elseif x == 1150 and y == -2023 and z == 69 then
		triggerClientEvent("onOffer", source, 420)
	elseif x == 1150 and y == -2018 and z == 69 then
		triggerClientEvent("onOffer", source, 601)
	end
end
addEventHandler("onPickupUse", root, pickupUse)
function markerUse(hitElement)
	local x,y,z = getElementPosition(source)
	outputConsole("Встал на маркер")
	triggerClientEvent("onOffer", source)
end
addEventHandler("onMarkerHit", root, markerUse)
function newLevel(thePlayer, commandName, lvl)
	triggerEvent("NewData", thePlayer, "players", "level", lvl)
	outputChatBox("Установлен уровень "..lvl)
end
addCommandHandler("setLevel", newLevel)

function spawnCar(thePlayer, commandName)
	local login = getElementData(root, "login", false)
	select_id = dbQuery(connectToPlayers, "SELECT id FROM players WHERE login=?", login)
		id = dbPoll(select_id, -1)
	select_car = dbQuery(connectToPlayers, "SELECT model_id FROM transport WHERE player_id=?", id[1].id)
		model = dbPoll(select_car, -1)
	if not model[1].model_id then
		outputChatBox("Транспорта нет")
	else
		local carX, carY, carZ = getElementPosition(thePlayer)
		createVehicle(model[1].model_id, carX, carY+5, carZ, 0, 0, 270, login)
	end
end
addCommandHandler("spawnTransport", spawnCar)