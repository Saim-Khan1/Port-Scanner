def getservbyport(port, protocol):
  with open("services.txt", 'r') as f:
    for line in f:
      if f"{port}/{protocol}" in line:
        return (line.split("	"))[0]
  return "unknown"