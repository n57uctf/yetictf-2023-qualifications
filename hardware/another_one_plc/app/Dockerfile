FROM golang:1.18-alpine as build_base

WORKDIR /tmp/plc

COPY ./main.go .

RUN go build -o ./out/main ./main.go

FROM alpine 

ENV ANOTHER_ONE_PLC_IP "0.0.0.0"
ENV ANOTHER_ONE_PLC_PORT "9600"
ENV ANOTHER_ONE_PLC_FLAG "YetiCTF{175_71m3_70_5ub5cr1b3_70_ru5c4d453c}"

COPY --from=build_base /tmp/plc/out/main /main

EXPOSE 9600/udp

CMD ["/main"]
