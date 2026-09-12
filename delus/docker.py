
# always save your code before the with closes
class Docker:
    class create_docker_environment:
        def __init__(self,base_image:str):
            self.code = ["FROM {}\n".format(base_image)]
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            self.code = []
        def environment_secrets(self,key:str,value:str):
            self.code.append("ENV {}={}\n".format(key,value))
        def build(self,command:str):
            self.code.append("RUN {}\n".format(command))
        def cmd(self,commands:list[str]):
            comand = ", ".join(['"{}"'.format(c) for c in commands])
            self.code.append("CMD [{}]\n".format(comand))
        def workdir(self,workdir:str):
            self.code.append("WORKDIR {}\n".format(workdir))
        def copy(self,source:str,destination:str):
            self.code.append("COPY {} {}\n".format(source,destination))
        def open_port(self,port:int):
            self.code.append("EXPOSE {}\n".format(port))
        def select_permissions(self,permission:str):
            self.code.append("USER {}\n".format(permission))
        def attach_persistent_storage(self,storage_path:str):
            self.code.append("VOLUME {}\n".format(storage_path))
        def entry_point(self,commands:list[str]):
            cmds = ", ".join(['"{}"'.format(c) for c in commands])
            self.code.append("ENTRYPOINT [{}]\n".format(cmds))
        def download_and_extract(self, url: str, destination: str):
            self.code.append("ADD {} {}\n".format(url, destination))
        def metadata(self, key: str, value: str):
            self.code.append("LABEL {}={}\n".format(key, value))
        def extract_docker_code(self):
            return "".join(self.code)

if __name__ == "__main__":
    docker = Docker()
    with docker.create_docker_environment("ubuntu:latest") as env:
        env.workdir("/app")
        env.copy(".",".")
        env.build("gcc main.c -o app")
        env.entry_point(["./app"])

        print(env.extract_docker_code())
