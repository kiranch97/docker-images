import { Server } from 'miragejs';

export function makeServer({ environment = 'development' } = {}) {
    let server = new Server({
        environment,

        routes() {
            this.urlPrefix = 'https://my.api.com:9999';
            this.get("/last_analysed_frames", () => {
                return { 
                    frame_meta: "foo",
                    take_frame: {
                        img: "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
                    },
                    detected_objects: [
                        {
                            detectedObjectType: "thrashbag",
                            bbox: {
                                coordinate1: 0,
                                coordinate2: 0
                            },
                            accuracy: 2
                        }
                    ]
                }
            })
            this.get("/detected_objects", () => {
                const detected_objects_by_type = {
                    garbage_bag: Math.floor((Math.random() * 100) + 1),
                    container_small: Math.floor((Math.random() * 100) + 1),
                    cardboard: Math.floor((Math.random() * 100) + 1),
                }

                return {
                    detected_objects_by_type,   
                    detected_objects: detected_objects_by_type.garbage_bag + 
                        detected_objects_by_type.container_small + 
                        detected_objects_by_type.cardboard
                }
            }, { timing: 10000 })
        },
    })

    return server
}