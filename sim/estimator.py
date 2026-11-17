"""
estimator.py — the estimator you built, shipped.
Intro to Autonomous Robotics (AUV) · Part I, Lectures 5 and 6 / Lab 4

These are the lines you typed in class, exactly as you typed them: the model
speaks (predict), the sensor speaks (correct), and Lecture 5's one-line filter
(predict_correct). Lab 4 imports them; nothing here is new.
"""
DT = 0.1                                         # tick length [s] -> 10 Hz, like the sensor
Q = 0.002 ** 2                                   # the model's lie per tick, squared: 2 mm -> 0.000004 m^2
R = 0.05 ** 2                                    # the sensor's lie, squared: sigma 5 cm -> 0.0025 m^2


def predict(est, P, w_prev):                     # the model speaks: move the belief, and blur it
    pred = max(0.0, est + (w_prev + 0.03) * DT)   # predict: run the physics one tick
    return pred, P + Q                           # two values back: the new belief, and its doubt grown by Q


def correct(pred, P, z):                         # the sensor speaks: blend by the numbers
    K = P / (P + R)                              # the gain: trust the sensor as much as we doubt ourselves
    nu = z - pred                                # the innovation: the sensor's surprise
    return pred + K * nu, (1 - K) * P            # the update: move K of the surprise; the doubt shrinks


def predict_correct(est, z, w_prev, g):          # the one-line filter, with a memory that MOVES
    pred = max(0.0, est + (w_prev + 0.03) * DT)   # predict: run the physics one tick
    return (1 - g) * pred + g * z                 # correct: nudge toward the evidence
