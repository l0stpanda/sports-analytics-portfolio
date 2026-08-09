from pybaseball import statcast

df = statcast(
    start_dt="2024-04-01",
    end_dt="2024-04-02"
)

print(df.head())
print(df.shape)