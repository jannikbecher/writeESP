srv = net.createServer(net.TCP, 180)
srv:listen(900, function(sck)
	sck:on("receive", function(sck, c)
		if file.open("test.lua", "a+") then
			file.write(c)
			file.close()
		end
	end)
	sck:on("disconnection", function(c)
		print("disconnect")
	end)
end)

