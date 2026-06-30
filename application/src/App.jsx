import {
  Activity,
  AlarmClock,
  Apple,
  ArrowLeft,
  BellRing,
  Bone,
  CalendarCheck,
  Check,
  ChevronRight,
  CircleHelp,
  Dumbbell,
  HeartPulse,
  Pause,
  Play,
  RotateCcw,
  Salad,
  ShieldCheck,
  ShieldPlus,
  SkipBack,
  SkipForward,
  Sparkles,
  TriangleAlert,
  User,
  Utensils,
  CircleUserRound,
  PersonStanding,
} from "lucide-react";
import { useMemo, useState } from "react";

const ASSET = (name) => `assets/${name}`;

const warmupPlans = [
  {
    id: "chest",
    title: "练胸日",
    subtitle: "启胸椎 · 唤肩胛",
    cue: "先打开胸椎，再让肩胛稳定。",
    minutes: 6,
    kcal: 2,
    actions: [
      { name: "肩胸激活", time: "1 分钟", goal: "激活肩袖 · 打开胸椎" },
      { name: "弹力带外旋", time: "1 分钟", goal: "稳定肩关节" },
      { name: "俯卧撑预备", time: "2 分钟", goal: "激活核心 · 稳定肩胛" },
      { name: "空杆推举", time: "2 分钟", goal: "提升动作模式" },
    ],
  },
  {
    id: "back",
    title: "练背日",
    subtitle: "开上背 · 找背阔",
    cue: "先打开上背，再找背阔发力。",
    minutes: 7,
    kcal: 3,
    actions: [
      { name: "猫牛伸展", time: "1 分钟", goal: "活动脊柱" },
      { name: "胸椎开书", time: "1 分钟", goal: "打开上背" },
      { name: "弹力带下拉", time: "2 分钟", goal: "唤醒背阔" },
      { name: "肩胛引体", time: "2 分钟", goal: "稳定肩胛" },
    ],
  },
  {
    id: "shoulder",
    title: "练肩日",
    subtitle: "热肩袖 · 稳关节",
    cue: "先热肩袖，再进入推举。",
    minutes: 6,
    kcal: 2,
    actions: [
      { name: "肩关节绕环", time: "1 分钟", goal: "活动肩关节" },
      { name: "弹力带拉开", time: "1 分钟", goal: "激活后束" },
      { name: "肩袖外旋", time: "2 分钟", goal: "唤醒肩袖" },
      { name: "墙面滑动", time: "2 分钟", goal: "改善上举路径" },
    ],
  },
  {
    id: "leg",
    title: "练腿日",
    subtitle: "开髋膝 · 稳步态",
    cue: "先打开髋膝踝，再做深蹲弓步。",
    minutes: 7,
    kcal: 3,
    actions: [
      { name: "髋部环绕", time: "1 分钟", goal: "打开髋部" },
      { name: "前后腿摆", time: "2 分钟", goal: "活动髋膝" },
      { name: "徒手深蹲", time: "2 分钟", goal: "唤醒腿部" },
      { name: "行走弓步", time: "2 分钟", goal: "激活全身协调" },
    ],
  },
  {
    id: "full",
    title: "练全身",
    subtitle: "轻快升温 · 醒节奏",
    cue: "先整体升温，再唤醒全身节奏。",
    minutes: 7,
    kcal: 3,
    actions: [
      { name: "轻快踏步", time: "1 分钟", goal: "提升心率" },
      { name: "侧向滑步", time: "2 分钟", goal: "唤醒协调" },
      { name: "虫爬到平板", time: "2 分钟", goal: "激活核心" },
      { name: "低冲击开合步", time: "2 分钟", goal: "综合热身" },
    ],
  },
];

const setupSteps = [
  { label: "性别", detail: "用于基础强度推荐" },
  { label: "身体", detail: "身高体重生成画像" },
  { label: "经历", detail: "决定讲解细度" },
  { label: "饮食", detail: "生成训练后建议" },
];

const readinessItems = [
  { id: "heart", label: "心率微微升高", icon: HeartPulse },
  { id: "joint", label: "关节活动顺畅", icon: Activity },
  { id: "breath", label: "呼吸节奏稳定", icon: ShieldCheck },
  { id: "body", label: "身体感觉良好", icon: Sparkles },
];

function App() {
  const [screen, setScreen] = useState("home");
  const [selectedId, setSelectedId] = useState("chest");
  const [setupStep, setSetupStep] = useState(0);
  const [gender, setGender] = useState("男");
  const [height, setHeight] = useState(168);
  const [weight, setWeight] = useState(58);
  const [sports, setSports] = useState(["力量训练", "几乎没有规律运动"]);
  const [wantsDiet, setWantsDiet] = useState(true);
  const [checks, setChecks] = useState({
    heart: true,
    joint: true,
    breath: true,
    body: true,
  });
  const [actionIndex, setActionIndex] = useState(0);
  const [paused, setPaused] = useState(false);

  const selectedPlan = useMemo(
    () => warmupPlans.find((plan) => plan.id === selectedId) ?? warmupPlans[0],
    [selectedId]
  );

  const readinessScore = Object.values(checks).filter(Boolean).length * 20 + 2;
  const allReady = Object.values(checks).every(Boolean);
  const currentAction = selectedPlan.actions[actionIndex];
  const warmupFlowScreens = ["home", "warmup", "readiness", "rest", "workout"];

  const navigate = (next) => {
    if (next === "workout") {
      setActionIndex(0);
      setPaused(false);
    }
    setScreen(next);
  };

  return (
    <main className="app">
      <section className="workspace">
        <SidePanel
          selectedPlan={selectedPlan}
          setScreen={setScreen}
          screen={screen}
          readinessScore={readinessScore}
          warmupFlowScreens={warmupFlowScreens}
        />

        <section className="phone-shell" aria-label="热身 App 交互预览">
          <StatusBar />
          {screen === "setup" && (
            <SetupScreen
              step={setupStep}
              setStep={setSetupStep}
              gender={gender}
              setGender={setGender}
              height={height}
              setHeight={setHeight}
              weight={weight}
              setWeight={setWeight}
              sports={sports}
              setSports={setSports}
              wantsDiet={wantsDiet}
              setWantsDiet={setWantsDiet}
              onFinish={() => navigate("home")}
            />
          )}
          {screen === "home" && (
            <HomeScreen
              selectedPlan={selectedPlan}
              onStart={() => navigate("warmup")}
              onSetup={() => navigate("setup")}
            />
          )}
          {screen === "warmup" && (
            <WarmupScreen
              selectedId={selectedId}
              setSelectedId={setSelectedId}
              selectedPlan={selectedPlan}
              onBack={() => navigate("home")}
              onStart={() => navigate("readiness")}
            />
          )}
          {screen === "readiness" && (
            <ReadinessScreen
              checks={checks}
              setChecks={setChecks}
              score={readinessScore}
              allReady={allReady}
              plan={selectedPlan}
              onBack={() => navigate("home")}
              onStart={() => navigate("workout")}
              onRest={() => navigate("rest")}
            />
          )}
          {screen === "rest" && (
            <RestScreen
              onBack={() => navigate("home")}
              onContinue={() => navigate("workout")}
              checks={checks}
            />
          )}
          {screen === "workout" && (
            <WorkoutScreen
              plan={selectedPlan}
              actionIndex={actionIndex}
              setActionIndex={setActionIndex}
              currentAction={currentAction}
              paused={paused}
              setPaused={setPaused}
              onFinish={() => navigate("profile")}
              onBack={() => navigate("readiness")}
            />
          )}
          {screen === "profile" && (
            <ProfileScreen
              plan={selectedPlan}
              onWarmup={() => navigate("home")}
            />
          )}
          {screen === "diet" && <DietScreen onBack={() => navigate("profile")} />}
          {screen !== "rest" && <BottomNav screen={screen} setScreen={navigate} />}
        </section>

        <ActionPanel
          selectedPlan={selectedPlan}
          readinessScore={readinessScore}
          screen={screen}
          onScreen={navigate}
        />
      </section>
    </main>
  );
}

function SidePanel({ selectedPlan, setScreen, screen, readinessScore, warmupFlowScreens }) {
  const isWarmupFlow = warmupFlowScreens.includes(screen);
  return (
    <aside className="side-panel">
      <div className="brand">
        <img src={ASSET("warmup-logo.png")} alt="热身 App logo" />
        <div>
          <strong>热身 App</strong>
          <span>训练前 8 分钟助手</span>
        </div>
      </div>
      <button className="notification" onClick={() => setScreen("home")}>
        <BellRing size={20} />
        <span>今日食谱已完成，快运动起来吧</span>
      </button>
      <div className="daily-card">
        <span>今日推荐</span>
        <h1>{selectedPlan.title}</h1>
        <p>{selectedPlan.cue}</p>
        <div className="metric-row">
          <b>{readinessScore}</b>
          <small>准备度</small>
          <b>{selectedPlan.minutes} 分钟</b>
          <small>预计时长</small>
        </div>
      </div>
      <nav className="quick-nav" aria-label="页面导航">
        {[
          ["home", "热身模块"],
          ["setup", "个性化设置"],
          ["profile", "我的主页"],
          ["diet", "饮食计划"],
        ].map(([id, label]) => (
          <button
            className={(id === "home" ? isWarmupFlow : screen === id) ? "active" : ""}
            key={id}
            onClick={() => setScreen(id)}
          >
            {label}
            <ChevronRight size={16} />
          </button>
        ))}
      </nav>
    </aside>
  );
}

function StatusBar() {
  return (
    <div className="status-bar">
      <span>9:41</span>
      <span className="signal">▮▮▮ ︶▱</span>
    </div>
  );
}

function ScreenHeader({ title, onBack, right }) {
  return (
    <header className="screen-header">
      {onBack ? (
        <button className="icon-btn" onClick={onBack} aria-label="返回">
          <ArrowLeft size={21} />
        </button>
      ) : (
        <span className="header-spacer" />
      )}
      <h2>{title}</h2>
      {right ?? <span className="header-spacer" />}
    </header>
  );
}

function HomeScreen({ selectedPlan, onStart, onSetup }) {
  return (
    <div className="screen-content home-screen">
      <div className="app-title">
        <img src={ASSET("warmup-logo-256.png")} alt="" />
        <div>
          <b>热身 App</b>
          <span>新手训练前的 8 分钟助手</span>
        </div>
        <button onClick={onSetup}>个性化</button>
      </div>
      <section className="hero-card">
        <div>
          <h1>今天先把身体叫醒</h1>
          <p>按训练日生成胸、背、肩、腿、全身热身，先热开再训练。</p>
          <div className="pill-row">
            <span>新手友好</span>
            <span>{selectedPlan.minutes} 分钟</span>
          </div>
        </div>
        <img src={ASSET("panda-coach.png")} alt="熊猫热身教练" />
      </section>
      <section className="home-flow-card">
        <span>今日推荐</span>
        <h2>{selectedPlan.title}</h2>
        <p>{selectedPlan.cue}</p>
        <div>
          <b>{selectedPlan.minutes} 分钟</b>
          <small>动态热身核心时长</small>
        </div>
      </section>
      <section className="home-step-row" aria-label="热身流程">
        {["选方向", "先自检", "再热身"].map((label, index) => (
          <span key={label}>
            <b>{index + 1}</b>
            {label}
          </span>
        ))}
      </section>
      <button className="primary-btn" onClick={onStart}>
        开始定制热身
        <ChevronRight size={20} />
      </button>
    </div>
  );
}

function WarmupScreen({ selectedId, setSelectedId, selectedPlan, onBack, onStart }) {
  return (
    <div className="screen-content">
      <ScreenHeader title="定制热身" onBack={onBack} />
      <section className="hero-card compact-hero">
        <div>
          <h1>{selectedPlan.title}</h1>
          <p>{selectedPlan.cue}</p>
          <div className="pill-row">
            <span>{selectedPlan.minutes} 分钟</span>
            <span>准备度 82</span>
          </div>
        </div>
        <img src={ASSET("panda-coach.png")} alt="熊猫热身教练" />
      </section>
      <section className="section-block">
        <div className="section-heading">
          <h2>选择今天练什么</h2>
          <span>减少误点</span>
        </div>
        <div className="warmup-grid">
          {warmupPlans.map((plan, index) => (
            <button
              className={selectedId === plan.id ? "warmup-option selected" : "warmup-option"}
              key={plan.id}
              onClick={() => setSelectedId(plan.id)}
            >
              <b>{index + 1}</b>
              <span>{plan.title}</span>
              <small>{plan.subtitle}</small>
            </button>
          ))}
        </div>
      </section>
      <button className="primary-btn" onClick={onStart}>
        进入热身自检
        <ChevronRight size={20} />
      </button>
    </div>
  );
}

function SetupScreen({
  step,
  setStep,
  gender,
  setGender,
  height,
  setHeight,
  weight,
  setWeight,
  sports,
  setSports,
  wantsDiet,
  setWantsDiet,
  onFinish,
}) {
  const next = () => {
    if (step === setupSteps.length - 1) onFinish();
    else setStep(step + 1);
  };

  const toggleSport = (sport) => {
    setSports((current) =>
      current.includes(sport)
        ? current.filter((item) => item !== sport)
        : [...current, sport]
    );
  };

  return (
    <div className="screen-content setup-screen">
      <ScreenHeader
        title="个性化设置"
        onBack={step > 0 ? () => setStep(step - 1) : undefined}
        right={<span className="step-tag">{step + 1}/4</span>}
      />
      <div className="progress-line">
        <span style={{ width: `${((step + 1) / setupSteps.length) * 100}%` }} />
      </div>
      <h1>{setupSteps[step].label}</h1>
      <p>{setupSteps[step].detail}</p>
      {step === 0 && (
        <div className="gender-choice">
          {[
            ["男", PersonStanding],
            ["女", CircleUserRound],
          ].map(([label, Icon]) => (
            <button
              key={label}
              className={gender === label ? "selected" : ""}
              onClick={() => setGender(label)}
            >
              <Icon size={38} />
              <span>{label}性</span>
            </button>
          ))}
        </div>
      )}
      {step === 1 && (
        <div className="range-list">
          <label>
            <span>身高</span>
            <b>{height} cm</b>
            <input
              type="range"
              min="150"
              max="190"
              value={height}
              onChange={(event) => setHeight(Number(event.target.value))}
            />
          </label>
          <label>
            <span>体重</span>
            <b>{weight} kg</b>
            <input
              type="range"
              min="42"
              max="90"
              value={weight}
              onChange={(event) => setWeight(Number(event.target.value))}
            />
          </label>
        </div>
      )}
      {step === 2 && (
        <div className="sports-list">
          {["力量训练", "跑步 / 有氧", "球类运动", "瑜伽 / 普拉提", "几乎没有规律运动"].map(
            (sport) => (
              <button
                key={sport}
                className={sports.includes(sport) ? "selected" : ""}
                onClick={() => toggleSport(sport)}
              >
                {sports.includes(sport) ? <Check size={19} /> : <PlusIcon />}
                <span>{sport}</span>
              </button>
            )
          )}
        </div>
      )}
      {step === 3 && (
        <div className="diet-choice">
          <button className={wantsDiet ? "selected" : ""} onClick={() => setWantsDiet(true)}>
            <Apple size={28} />
            <div>
              <b>是，帮我定制</b>
              <span>为您生成好，放到我的主页里面。</span>
            </div>
          </button>
          <button className={!wantsDiet ? "selected" : ""} onClick={() => setWantsDiet(false)}>
            <Dumbbell size={28} />
            <div>
              <b>暂时不用</b>
              <span>可以直接进入训练啦！</span>
            </div>
          </button>
        </div>
      )}
      <button className="primary-btn" onClick={next}>
        {step === setupSteps.length - 1 ? "生成我的热身方案" : "下一步"}
        <ChevronRight size={20} />
      </button>
    </div>
  );
}

function PlusIcon() {
  return <span className="plus-icon">+</span>;
}

function ReadinessScreen({ checks, setChecks, score, allReady, plan, onBack, onStart, onRest }) {
  return (
    <div className="screen-content">
      <ScreenHeader title="热身前自检" onBack={onBack} />
      <section className="coach-card">
        <img src={ASSET("panda-small.png")} alt="熊猫教练" />
        <div>
          <span>AI 熊猫提醒</span>
          <p>先确认身体状态，再进入热身。</p>
        </div>
      </section>
      <section className="check-card">
        <div className="section-heading">
          <h2>准备度自检</h2>
          <span>{plan.title}</span>
        </div>
        {readinessItems.map(({ id, label, icon: Icon }) => (
          <button
            className={checks[id] ? "check-row checked" : "check-row"}
            key={id}
            onClick={() => setChecks((current) => ({ ...current, [id]: !current[id] }))}
          >
            <span>{checks[id] ? <Check size={18} /> : "!"}</span>
            <b>{label}</b>
            <Icon size={24} />
          </button>
        ))}
      </section>
      <section className="score-card">
        <div className="score-ring">{score}</div>
        <div>
          <b>准备度 {score}</b>
          <p>{allReady ? "状态不错，可以开始热身！" : "检测到不适反馈，建议今天先休息。"}</p>
        </div>
      </section>
      {allReady ? (
        <button className="primary-btn" onClick={onStart}>
          开始动态热身
          <Play size={20} />
        </button>
      ) : (
        <button className="warning-btn" onClick={onRest}>
          查看休息建议
          <ChevronRight size={20} />
        </button>
      )}
    </div>
  );
}

function RestScreen({ onBack, onContinue, checks }) {
  const discomfortLabels = {
    heart: "心率异常",
    joint: "关节不适",
    breath: "呼吸不稳",
    body: "身体不适",
  };
  const discomforts = readinessItems
    .filter((item) => !checks[item.id])
    .map((item) => discomfortLabels[item.id]);
  const visibleDiscomforts = discomforts.length > 0 ? discomforts : ["关节不适", "呼吸不稳"];

  return (
    <div className="screen-content rest-screen">
      <ScreenHeader
        title="今日建议休息"
        onBack={onBack}
        right={
          <button className="help-btn" aria-label="帮助">
            <CircleHelp size={21} />
          </button>
        }
      />
      <div className="rest-hero-panda">
        <img src={ASSET("panda-small.png")} alt="熊猫关心提示" />
      </div>
      <section className="rest-warning-card">
        <div>
          <span>
            <TriangleAlert size={20} />
            检测到不适反馈
          </span>
          <h1>今天先不训练</h1>
          <p>身体状态比完成训练更重要，建议休息并择日再练。</p>
        </div>
        <HeartPulse size={72} />
      </section>
      <section className="discomfort-card">
        <h2>你反馈的不适</h2>
        <div>
          {visibleDiscomforts.slice(0, 2).map((item, index) => (
            <span key={item}>
              {index === 0 ? <Bone size={26} /> : <HeartPulse size={26} />}
              {item}
            </span>
          ))}
        </div>
      </section>
      <section className="comfort-card">
        <img src={ASSET("panda-small.png")} alt="" />
        <p>
          休息不是偷懒，<br />
          而是为了更好的进步。<br />
          照顾好自己，我们下次见！
        </p>
      </section>
      <button className="primary-btn" onClick={onBack}>
        <CalendarCheck size={22} />
        记录并返回计划
      </button>
      <button className="danger-btn" onClick={onContinue}>
        <AlarmClock size={20} />
        我还想继续训练
      </button>
      <section className="medical-note">
        <ShieldPlus size={20} />
        如疼痛持续，请咨询专业人士
      </section>
    </div>
  );
}

function WorkoutScreen({
  plan,
  actionIndex,
  setActionIndex,
  currentAction,
  paused,
  setPaused,
  onFinish,
  onBack,
}) {
  const progress = ((actionIndex + 1) / plan.actions.length) * 100;

  const nextAction = () => {
    if (actionIndex === plan.actions.length - 1) onFinish();
    else setActionIndex(actionIndex + 1);
  };

  return (
    <div className="screen-content workout-screen">
      <ScreenHeader title={`${actionIndex + 1}/${plan.actions.length} ${currentAction.name}`} onBack={onBack} />
      <div className="mini-progress">
        <span style={{ width: `${progress}%` }} />
      </div>
      <div className="workout-metrics">
        <div>
          <b>00:{32 + actionIndex * 22}</b>
          <span>运动时长</span>
        </div>
        <div>
          <b>{plan.kcal} 千卡</b>
          <span>预计消耗</span>
        </div>
      </div>
      <section className="panda-stage">
        <img src={ASSET("panda-coach.png")} alt="熊猫示范动作" />
        <strong>25"</strong>
      </section>
      <button className="feedback-pill">
        <span>反馈</span>
        练得怎么样 ~
      </button>
      <div className="player-controls">
        <button
          onClick={() => setActionIndex(Math.max(0, actionIndex - 1))}
          aria-label="上一个动作"
        >
          <SkipBack size={22} />
        </button>
        <button className="pause-button" onClick={() => setPaused(!paused)} aria-label="暂停或继续">
          {paused ? <Play size={30} /> : <Pause size={30} />}
        </button>
        <button onClick={nextAction} aria-label="下一个动作">
          <SkipForward size={22} />
        </button>
      </div>
      <section className="tip-strip">
        <Activity size={17} />
        <span>{currentAction.goal}，保持呼吸稳定。</span>
      </section>
    </div>
  );
}

function ProfileScreen({ plan, onWarmup }) {
  return (
    <div className="screen-content profile-screen">
      <div className="profile-header">
        <div>
          <img src={ASSET("warmup-logo-256.png")} alt="" />
          <span>我的</span>
        </div>
        <button>编辑资料</button>
      </div>
      <section className="user-card">
        <img src={ASSET("panda-small.png")} alt="用户头像" />
        <div>
          <h1>小暖同学</h1>
          <p>新手热身 · 连续 3 天</p>
          <span>准备度 82</span>
        </div>
      </section>
      <section className="today-card">
        <div>
          <span>今日完成</span>
          <h2>{plan.title}动态热身</h2>
          <p>{plan.actions.map((item) => item.name).join(" · ")}</p>
        </div>
        <b>{plan.minutes} 分钟</b>
        <div className="steps">
          {plan.actions.map((_, index) => (
            <span key={index}>{index + 1}</span>
          ))}
        </div>
      </section>
      <div className="stats-grid">
        <StatCard label="本周热身" value="3 次" tag="周" />
        <StatCard label="累计时长" value="24 分钟" tag="时" />
        <StatCard label="平均准备度" value="82" tag="分" />
        <StatCard label="完成率" value="92%" tag="率" />
      </div>
      <section className="records-card">
        <div className="section-heading">
          <h2>最近热身记录</h2>
          <button onClick={onWarmup}>查看全部</button>
        </div>
        {["胸日热身", "全身热身", "肩日热身"].map((record, index) => (
          <div className="record-row" key={record}>
            <Check size={18} />
            <span>
              <b>{record}</b>
              <small>{index === 2 ? "3/4 动作 · 跳过 1 个" : "4/4 动作 · 状态良好"}</small>
            </span>
            <em>{index === 0 ? "今天 18:42" : index === 1 ? "昨天 19:10" : "周一 18:55"}</em>
          </div>
        ))}
      </section>
    </div>
  );
}

function StatCard({ label, value, tag }) {
  return (
    <section className="stat-card">
      <span>{label}</span>
      <b>{value}</b>
      <em>{tag}</em>
    </section>
  );
}

function DietScreen({ onBack }) {
  return (
    <div className="screen-content diet-screen">
      <ScreenHeader title="训练后饮食计划" onBack={onBack} />
      <section className="diet-hero">
        <Salad size={42} />
        <div>
          <h1>今日食谱已完成</h1>
          <p>快运动起来吧。训练后按这份食谱吃，帮身体稳定恢复。</p>
        </div>
      </section>
      <div className="macro-grid">
        <StatCard label="目标热量" value="1650 kcal" tag="日" />
        <StatCard label="蛋白质" value="95 g" tag="优" />
      </div>
      {[
        ["早餐", "鸡蛋 + 全麦吐司 + 无糖酸奶"],
        ["午餐", "米饭半碗 + 鸡胸/牛肉 + 两份蔬菜"],
        ["训练后", "香蕉或酸奶，30 分钟内补充水分"],
        ["晚餐", "鱼虾豆腐任选其一，主食不过量"],
      ].map(([meal, detail]) => (
        <section className="meal-row" key={meal}>
          <span>{meal}</span>
          <p>{detail}</p>
        </section>
      ))}
      <button className="primary-btn" onClick={onBack}>
        返回我的主页
      </button>
    </div>
  );
}

function BottomNav({ screen, setScreen }) {
  const isWarmupFlow = ["home", "warmup", "readiness", "rest", "workout"].includes(screen);
  return (
    <nav className="bottom-nav" aria-label="底部导航">
      <button className={screen === "profile" ? "active" : ""} onClick={() => setScreen("profile")}>
        <User size={18} />
        我的
      </button>
      <button className={isWarmupFlow ? "active" : ""} onClick={() => setScreen("home")}>
        <Activity size={18} />
        热身
      </button>
      <button className={screen === "diet" ? "active" : ""} onClick={() => setScreen("diet")}>
        <Utensils size={18} />
        饮食
      </button>
    </nav>
  );
}

function ActionPanel({ selectedPlan, readinessScore, screen, onScreen }) {
  return (
    <aside className="action-panel">
      <div className="panel-card">
        <span>当前流程</span>
        <h2>{screenLabel(screen)}</h2>
        <p>按 PRD 逻辑：早上食谱提醒召回，首页进入热身模块，再完成方向选择、自检和动态热身。</p>
      </div>
      <div className="panel-card compact">
        <AlarmClock size={22} />
        <div>
          <b>每日 08:00</b>
          <p>今日食谱已完成，快运动起来吧</p>
        </div>
      </div>
      <div className="panel-card">
        <span>本次热身</span>
        <h3>{selectedPlan.title}</h3>
        <ul>
          {selectedPlan.actions.map((action) => (
            <li key={action.name}>
              <Check size={16} />
              {action.name}
            </li>
          ))}
        </ul>
      </div>
      <div className="panel-actions">
        <button onClick={() => onScreen("warmup")}>开始定制热身</button>
        <button onClick={() => onScreen("profile")}>查看我的数据</button>
        <button onClick={() => onScreen("diet")}>查看饮食计划</button>
      </div>
      <div className="readiness-mini">
        <RotateCcw size={18} />
        <span>准备度 {readinessScore}</span>
      </div>
    </aside>
  );
}

function screenLabel(screen) {
  const labels = {
    setup: "个性化设置",
    home: "热身首页",
    warmup: "热身方向选择",
    readiness: "热身前自检",
    rest: "不适提示",
    workout: "动态热身",
    profile: "我的主页",
    diet: "饮食计划",
  };
  return labels[screen] ?? "热身方向选择";
}

export default App;
