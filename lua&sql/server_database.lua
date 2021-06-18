function Connection()
	connectToPlayers = dbConnect("mysql", "dbname=server_mta;host=127.0.0.1;port=3306", "root", "password")
	if connectToPlayers then
		outputConsole("Подключилось")
	else
		outputConsole("Не подключилось")
	end
end
addEventHandler("onResourceStart", getResourceRootElement(getThisResource()), Connection)
function StopConnection()
    destroyElement(connectToPlayers)
	outputConsole("Соединение с БД остановлено")
end
addEventHandler("onResourceStop", root, StopConnection)
function Registration(login, password)
	serial = getPlayerSerial(source)
	check_serial = dbQuery(connectToPlayers, "SELECT COUNT(reg_serial) AS `ser` FROM technical_info WHERE reg_serial=?", serial)
	result_serial = dbPoll(check_serial, -1)
	if result_serial then
		outputConsole("Игроков с данным серийником: "..result_serial[1].ser)
	else
		outputConsole("Нет ответа о серийнике")
		dbFree(result_serial)
	end
	--[[IP = getPlayerIP(thePlayer)
	check_IP = dbQuery(connectToPlayers, "SELECT COUNT(reg_adress) AS `ip` FROM technical_info WHERE reg_adress=?", IP)
	result_adress = dbPoll(check_IP, -1)
	if result_serial then
		outputChatBox("Игроков с данным адресом: "..result_adress[1].ip)
	else
		outputChatBox("Нет ответа об адресе")
		dbFree(result_adress)
	end]]
	check_log = dbQuery(connectToPlayers, "SELECT login FROM players WHERE login=?", login)
	result_log = dbPoll(check_log, -1)
	if result_log then
		if #result_log >= 1 then
			triggerClientEvent("AnswerReg", source, "Логин существует")
		else
			newplayer = dbExec(connectToPlayers, "INSERT INTO players(login, password) VALUES (?,?)", login, password)
			select_id = dbQuery(connectToPlayers, "SELECT id FROM players WHERE login=?", login)
			id = dbPoll(select_id, -1)
			newinfo = dbExec(connectToPlayers, "INSERT INTO technical_info(reg_serial, player_id) VALUES (?,?)", serial,id[1].id)
			id_transp = dbExec(connectToPlayers, "INSERT INTO transport(player_id) VALUES (?)", id[1].id)
			id_weapon = dbExec(connectToPlayers, "INSERT INTO weapons(player_id) VALUES (?)", id[1].id)
			id_skills = dbExec(connectToPlayers, "INSERT INTO skills(player_id) VALUES (?)", id[1].id)
			if newplayer and newinfo and id_transp and id_weapon and id_skills then
				triggerClientEvent("AnswerReg", source, "Новый игрок зарегестрирован")
			else
				triggerClientEvent("AnswerReg", source, "Не добавлен")
				dbFree(select_id)
			end
		end
	else
		triggerClientEvent("AnswerReg", source, "Нет ответа о логине")
		dbFree(result_log)
	end
end
addEvent("RegNewPlayer", true)
addEventHandler("RegNewPlayer", root, Registration)
function Login(login, password)
	select_account = dbQuery(connectToPlayers, "SELECT login FROM players WHERE login=? and password=?", login, password)
	account = dbPoll(select_account, -1)
	if #account < 1 then
		triggerClientEvent("AnswerLog", source, "Не верные данные для входа", -1)
	else
		select_fraction = dbQuery(connectToPlayers, "SELECT fraction FROM players WHERE login=?", login)
		fraction = dbPoll(select_fraction, -1)
		if fraction[1].fraction == 0 then
			triggerClientEvent("AnswerLog", source, "Фракция не выбрана", fraction[1].fraction)
		else			
			select_skin = dbQuery(connectToPlayers, "SELECT skin FROM players WHERE login=?", login)
			skin = dbPoll(select_skin, -1)
			select_money = dbQuery(connectToPlayers, "SELECT money FROM players WHERE login=?", login)
			money = dbPoll(select_money, -1)
			if fraction[1].fraction == 1 then
				X, Y, Z = 1136, -2034.5, 69
			elseif fraction[1].fraction == 2 then
				X, Y, Z = -2287.5, 155.5, 35
			end
			triggerEvent("spawnPlayer", source, X, Y, Z, 270, skin[1].skin, money[1].money)
			triggerClientEvent("AnswerLog", source, "Персонаж ранее создан", -1)
		end
	end
end
addEvent("onLogin", true)
addEventHandler("onLogin", root, Login)
function UpData(tablename, column, value)
	local login = getElementData(root, "login", false)
	dbExec(connectToPlayers, "UPDATE `??` SET `??`=? WHERE login=?", tablename, column, value, login)
end
addEvent("NewData", true)
addEventHandler("NewData", root, UpData)
function CheckTransport(car)
	local login = getElementData(root, "login", false)
	select_id = dbQuery(connectToPlayers, "SELECT id FROM players WHERE login=?", login)
		id = dbPoll(select_id, -1)
	select_idTr = dbQuery(connectToPlayers, "SELECT model_id FROM transport WHERE player_id=?", id[1].id)
		idTr = dbPoll(select_idTr, -1)
	if idTr[1].model_id then
		outputChatBox("Транспорт уже есть")
	else
		outputChatBox("Транспорт куплен")
		local select_money = dbQuery(connectToPlayers, "SELECT money FROM players WHERE login=?", login)
		local money = dbPoll(select_money, -1)
		local balance = money[1].money - 50000
		setPlayerMoney(source, balance, false)
		--triggerEvent("NewData", source, "transport", "model_id", idTr[1].model_id)
		dbExec(connectToPlayers, "UPDATE `??` SET `??`=? WHERE player_id=?", "transport", "model_id", car, id[1].id)
		triggerEvent("NewData", source, "players", "money", balance)
	end
end
addEvent("checkTr", true)
addEventHandler("checkTr", root, CheckTransport)