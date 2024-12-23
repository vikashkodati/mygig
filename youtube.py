"""Script to find YouTube channels and create TikTok hooks using CrewAI agents."""

from crewai import Agent, Task, Process, Crew
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
    role='Senior Researcher',
    goal='Uncover the best Youtube channels for beginners who want to learn about: {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of innovation. "
        "You love sharing knowledge with beginners who are just starting out. "
        "You have a passion for geospatial technology, AI, ML and solving problems."
        "You believe geospatial technology helps solve humanitarian problems."
        "You are a big fan of the Open Source Geospatial Foundation (OSGeo) and the USGIS."
        "You love educating people on how to fine tune and train geospatial foundation models."
    ),
    tools=[search_tool],
    allow_delegation=True,
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
    role='Writer',
    goal='Create short viral TikTok scripts about why you should learning {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned copywriter with a knack for writing short viral TikTok hooks. "
        "You know how to instantly get people's attention and make them want to learn more."
    ),
    tools=[search_tool],
    allow_delegation=False,
)

# Research task
research_task = Task(
    description=(
        "Identify the best {number} Youtube channels for beginners to learn {topic}. "
        "Focus on finding Youtube channels for beginners who know nothing about {topic}. "
        "Your final list should explain the focus of each channel. "
        "Your research will help a founder of a startup building niche foundation models to support observation from satellites/space."
        "You will help them find the best Youtube channels to learn about the basics of geospatial technology, AI, ML and solving problems."
    ),
    expected_output=  'A list of {number} Youtube channels, each with a 2-sentence description of what makes the channel unique.',
    agent=researcher
)

# Writing task with language model configuration
write_task = Task(
    description=(
        "Using the insights provided from the Research Task, write a 20-word viral TikTok hook about learning: {topic}. "
        "Focus on why it's important to learn about {topic} and negative consequences of not learning. "
        "This script should spark curiosity and make viewers stop scrolling to learn more."
    ),
    expected_output='A persuasive TikTok hook that makes beginners want to learn {topic}. Do not include emojis or hashtags.',
    agent=writer,
    async_execution=False,
    output_file='new-tiktok-script.md'  # Example of output customization
)

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Optional: Sequential task execution is default
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'finetune a geospatial foundation model', 'number': 15})
print(result)
