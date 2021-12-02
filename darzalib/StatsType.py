class GmPacketTypes:
    Unknown = 0
    Update = 1
    Hello = 2
    Load = 3
    Create = 4
    Ping = 5
    Pong = 6
    UseItem = 7
    ProjHit = 8
    EnterPortal = 9
    Move = 10
    CharInfo = 11
    Register = 12
    RegisterResp = 13
    MapInfo = 14
    Shoot = 15
    Message = 16
    Swap = 17
    TakeItem = 18
    Tiles = 19
    Chat = 20
    Drop = 21
    StartUpdate = 22
    ChangeName = 23
    Buy = 24
    Quest = 25
    Goto = 26
    Death = 27
    GcAuth = 28
    GcSwitch = 29
    GcReq = 30
    GcRes = 31
    Tick = 32
    TradeRequest = 33
    TradeFinished = 34
    TradeChanged = 35
    TradeStart = 36
    HelloResp = 37
    LeaderboardResp = 38
    GetLeaderboard = 39
    GetProducts = 40
    ProductsResp = 41
    VerifyIap = 42
    PlayEffect = 43
    GetServers = 44
    Reconnect = 45
    CreateGuild = 46
    InviteGuild = 47
    JoinGuild = 48
    GetNews = 49
    NewsResp = 50
    UpdateAssets = 51
    AssetVersions = 52
    GotoResp = 53
    Revive = 54
    ReviveResp = 55
    GetDeaths = 56
    DeathsResp = 57
    VerifyIapResp = 58
    CollectGold = 59
    DailyGold = 60
    VerifyDroidIap = 61
    UpdateGold = 62
    Ad = 63
    ServerList = 64
    LeaveGuild = 65
    ChallengeUpdated = 66
    Aoe = 67
    GuildListResp = 68
    GetGuildList = 69
    GuildModify = 70
    GuildTakeBanner = 71
    HealthUpdate = 72
    IosDeviceToken = 73
    GuildMessage = 74
    GuildModifyResp = 75
    LinkEmail = 76
    LinkEmailResp = 77
    RecoverEmail = 78
    RecoverEmailResp = 79
    TickAck = 80
    UpdateAck = 81
    ActivateObject = 82
    Disconnect = 83
    Projectiles = 84
    Chats = 85
    Messages = 86
    ProjectilesAck = 87
    AllyHit = 88
    Escape = 89
    UseItemAck = 90
    SwapAck = 91
    CreateResp = 92
    TradeItems = 93
    UnlockedClass = 94
    BiomeDisplay = 95
    UpdateEssences = 96
    DiscoverEssence = 97
    EditEssence = 98
    SelectEssenceResp = 99
    ExchangeEssence = 100
    ExchangeEssenceResp = 101
    ExchangeGift = 102
    ExchangeGiftAck = 103
    Failure = 104
    WorldDisplay = 105
    CheckPing = 106
    CheckPingAck = 107
    SetMusic = 108
    MapInfoAck = 109
    reverseDict = {x[1]: x[0] for x in locals().items() if isinstance(x[1], int)}